import json
import re
import requests

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, reverse, get_object_or_404

from accounts.models import CustomUser
from hackathon.models import Hackathon, HackTeam, HackProject
from teams.helpers import choose_team_sizes, group_participants,\
                          choose_team_levels, find_all_combinations,\
                          distribute_participants_to_teams,\
                          create_teams_in_view, update_team_participants
from teams.forms import HackProjectForm, EditTeamName

SLACK_GROUP_IM_ENDPOINT = 'https://slack.com/api/conversations.open/'


@login_required
def change_teams(request, hackathon_id):
    """ Page that handles the logic of automatically distributing the teams
    for a hackathon and allows for the admin to re-arrange the team members """
    # Redirect user if they are not admin
    if not request.user.is_superuser:
        return redirect(reverse('hackathon:view_hackathon',
                                kwargs={'hackathon_id': hackathon_id}))

    edit = False
    hackathon = Hackathon.objects.get(id=hackathon_id)
    participants = hackathon.participants.all()

    if len(participants) == 0:
        teams = []
        participants_still_to_distribute = []
    elif len(hackathon.teams.all()) == 0:
        team_size = hackathon.team_size
        team_sizes = sorted(choose_team_sizes(participants, team_size))
        if len(team_sizes) == 0:
            return render(request, 'change_teams.html',
                        {'num_participants': len(participants)})
        grouped_participants, hackathon_level = group_participants(
            participants, len(team_sizes))
        team_levels = sorted(choose_team_levels(len(team_sizes), hackathon_level))
        combos_without_dupes = find_all_combinations(
            participants, team_sizes)
        teams, leftover_participants = distribute_participants_to_teams(
            team_sizes, team_levels, grouped_participants,
            combos_without_dupes)
        participants_still_to_distribute = [
            participant for participant_groups in leftover_participants.values()
            for participant in participant_groups]
    else:
        edit = True
        teams = hackathon.teams.all()
        team_members = [user for team in teams
                        for user in team.participants.all()]
        participants_still_to_distribute = [participant.to_team_member()
                                            for participant in participants
                                            if participant not in team_members]
        teams = {team.display_name: [
                    team_member.to_team_member()
                    for team_member in team.participants.all()]
                 for team in teams}

    return render(request, 'change_teams.html', {
        'hackathon_id': hackathon_id,
        'num_participants': len(participants), 
        'teams': teams,
        'leftover_participants': participants_still_to_distribute,
        'edit': edit,
        })


@login_required
def create_teams(request):
    """ View used to save the hackathon teams created by an admin """
    if not request.user.is_superuser:
        messages.error(request, "You do not have access to this page!")
        return redirect(reverse('hackathon:hackathon-list'))

    if request.method == 'POST':
        data = request.POST
        teams = json.loads(data.get('teams'))
        hackathon_id = data.get('hackathon_id')

        if data.get('_method') == 'post':
            with transaction.atomic():
                create_teams_in_view(request.user, teams, hackathon_id)
                messages.success(request, "Teams assigned successfully!")
            return redirect(reverse('hackathon:view_hackathon',
                                    kwargs={'hackathon_id': hackathon_id}))
        else:
            with transaction.atomic():
                update_team_participants(request.user, teams, hackathon_id)
                messages.success(request, "Teams updated successfully!")
            return redirect(reverse('hackathon:view_hackathon',
                                    kwargs={'hackathon_id': hackathon_id}))
    else: 
        return redirect(reverse('hackathon:hackathon-list'))


@login_required
def clear_teams(request):
    if not request.user.is_superuser:
        messages.error(request, "You do not have access to this page!")
        return redirect(reverse('hackathon:hackathon-list'))

    if request.method == 'POST':
        data = request.POST
        hackathon_id = data.get('hackathon_id')
        hackathon = Hackathon.objects.get(id=hackathon_id)
        for team in hackathon.teams.all():
            team.delete()
        return redirect(reverse('hackathon:change_teams',
                                kwargs={'hackathon_id': hackathon_id}))
    else: 
        return redirect(reverse('hackathon:hackathon-list'))


@login_required
def view_team(request, team_id):
    """ View the detailed team information for a HackTeam """
    team = get_object_or_404(HackTeam, id=team_id)
    rename_team_form = EditTeamName(instance=team)
    create_group_im = (settings.SLACK_ENABLED and settings.SLACK_BOT_TOKEN)

    return render(request, 'team.html', {
        'team': team,
        'rename_team_form': rename_team_form,
        'create_group_im': create_group_im,
        })


@login_required
def create_project(request, team_id):
    """ Create a new HackProject for a team """
    hack_team = get_object_or_404(HackTeam, id=team_id)
    hack_project = HackProject.objects.filter(hackteam=hack_team)

    if hack_team.hackathon.status != 'hack_in_progress':
        messages.error(request, "You currently cannot edit this project.")
        return redirect(reverse('view_team', kwargs={'team_id': team_id}))

    if request.method == 'POST':
        if hack_project: 
            form = HackProjectForm(request.POST, instance=hack_project.get())
        else:
            form = HackProjectForm(request.POST)

        if form.is_valid():
            hack_project = form.save()
            hack_team.project = hack_project
            hack_team.save()

            messages.success(request, 'Project updated successfully.')
            return redirect(reverse('view_team', kwargs={'team_id': team_id}))
        else:
            messages.error(request, ('An unexpected error occurred updating '
                                     'the project. Please try again.'))
            return redirect(reverse('view_team', kwargs={'team_id': team_id}))
    else:
        if hack_project:
            form = HackProjectForm(instance=hack_project.get())
        else:
            form = HackProjectForm()

    return render(request, 'create_project.html', {
        'form': form,
        'team_id': team_id
    })


@login_required
def rename_team(request, team_id):
    """ Change the name of a HackTeam """
    hack_team = get_object_or_404(HackTeam, id=team_id)

    if (not request.user.is_staff 
            and request.user not in hack_team.participants.all()):
        messages.error(request,
                       'You do not have access to rename this team')
        return redirect(reverse('view_team', kwargs={'team_id': team_id}))
    
    form = EditTeamName(request.POST, instance=hack_team)
    if form.is_valid():
        form.save()
        messages.success(request,
                         'Team renamed successfully.')
    else:
        messages.error(request,
                       'An unexpected error occurred.')
    return redirect(reverse('view_team', kwargs={'team_id': team_id}))


@login_required
def create_group_im(request, team_id):
    """ Creates a new group IM in slack """
    if request.method != 'POST':
        messages.error(request,
                       'You cannot access this page in this way.')
        return redirect(reverse('view_team', kwargs={'team_id': team_id}))

    team = get_object_or_404(HackTeam, id=team_id)
    if not (request.user in team.participants.all()
            or request.user == team.mentor):
        messages.error(request,
                       ('You do not have access to create a Slack IM group '
                       'for this team.'))
        return redirect(reverse('view_team', kwargs={'team_id': team_id}))

    if not (settings.SLACK_ENABLED or settings.SLACK_BOT_TOKEN
            or settings.SLACK_WORKSPACE):
        messages.error(request, 'This feature is currently not enabled.')
        return redirect(reverse('view_team', kwargs={'team_id': team_id}))   

    pattern = re.compile(r'^U[a-zA-Z0-9]*[_]T[a-zA-Z0-9]*$')
    users = [team_member.username.split('_')[0] 
             for team_member in team.participants.all()
             if pattern.match(team_member.username)]

    if team.mentor:
        users.append(team.mentor.username.split('_')[0])

    params = {
        'users': ','.join(users),
    }
    headers = {'Authorization': f'Bearer {settings.SLACK_BOT_TOKEN}' }
    response = requests.get(SLACK_GROUP_IM_ENDPOINT, params=params,
                             headers=headers)

    if not response.status_code == 200:
        messages.error(request, ('An unexpected error occurred creating the '
                                 'Group IM.'))
        return redirect(reverse('view_team', kwargs={'team_id': team_id}))

    response = response.json()
    if not response.get('ok'):
        messages.error(request, (f'An error occurred creating the Group IM. '
                                 f'Error code: {response.get("error")}'))
        return redirect(reverse('view_team', kwargs={'team_id': team_id}))
        
    channel = response.get('channel', {}).get('id')
    communication_channel = (f'https://{settings.SLACK_WORKSPACE}.slack.com/'
                             f'app_redirect?channel={channel}')
    team.communication_channel = communication_channel
    team.save()

    if len(users) < len(team.participants.all()):
        missing_users = len(team.participants.all()) - len(users)
        messages.error(request, 
                       (f'Group IM successfully created, but {missing_users} '
                        f'users could not be added to the Group IM. '
                        f'Please add the missing users manually.'))
    else:
        messages.success(request, 'Group IM successfully created')

    return redirect(reverse('view_team', kwargs={'team_id': team_id}))
