from datetime import datetime, timedelta
import json
import pytz
import re
import requests

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, reverse, get_object_or_404

from accounts.decorators import can_access, has_access_to_team
from accounts.models import UserType, SlackSiteSettings
from accounts.lists import TIMEZONE_CHOICES
from competencies.models import Competency
from hackathon.models import Hackathon, HackTeam, HackProject
from teams.helpers import (
    choose_team_sizes, group_participants,
    choose_team_levels, find_all_combinations,
    distribute_participants_to_teams,
    create_teams_in_view, update_team_participants,
    calculate_timezone_offset, invite_users_to_slack_channel)
from teams.forms import HackProjectForm, EditTeamName

SLACK_CHANNEL_ENDPOINT = 'https://slack.com/api/conversations.create'
SLACK_CHANNEL_INVITE_ENDPOINT = 'https://slack.com/api/conversations.invite'


@login_required
@can_access([UserType.SUPERUSER, UserType.FACILITATOR_ADMIN,
             UserType.PARTNER_ADMIN],
            redirect_url='hackathon:hackathon-list')
def change_teams(request, hackathon_id):
    """ Page that handles the logic of automatically distributing the teams
    for a hackathon and allows for the admin to re-arrange the team members """
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
@can_access([UserType.SUPERUSER, UserType.FACILITATOR_ADMIN,
             UserType.PARTNER_ADMIN],
            redirect_url='hackathon:hackathon-list')
def create_teams(request):
    """ View used to save the hackathon teams created by an admin """
    if request.method == 'POST':
        data = request.POST
        teams = json.loads(data.get('teams'))
        hackathon_id = data.get('hackathon_id')

        if data.get('_method') == 'post':
            with transaction.atomic():
                create_teams_in_view(request.user, teams, hackathon_id)
                messages.success(request, "Teams assigned successfully!")
            return redirect(reverse('hackathon:change_teams',
                                    kwargs={'hackathon_id': hackathon_id}))
        else:
            with transaction.atomic():
                update_team_participants(request.user, teams, hackathon_id)
                messages.success(request, "Teams updated successfully!")
            return redirect(reverse('hackathon:change_teams',
                                    kwargs={'hackathon_id': hackathon_id}))
    else:
        return redirect(reverse('hackathon:hackathon-list'))


@login_required
@can_access([UserType.SUPERUSER, UserType.FACILITATOR_ADMIN,
             UserType.PARTNER_ADMIN],
            redirect_url='hackathon:hackathon-list')
def clear_teams(request):
    """ Reset all teams for a specific hackathon """
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
@has_access_to_team()
def view_team(request, team_id):
    """ View the detailed team information for a HackTeam """
    team = get_object_or_404(HackTeam, id=team_id)
    non_participant_superuser = (
        (request.user.is_superuser or request.user.is_staff)
        and not request.user.is_participant(team.hackathon))
    rename_team_form = EditTeamName(instance=team)
    create_private_channel = (settings.SLACK_ENABLED is not None
                              and settings.SLACK_BOT_TOKEN is not None
                              and settings.SLACK_ADMIN_TOKEN is not None)

    mentor_profile = None
    if team.mentor and settings.SLACK_WORKSPACE:
        mentor_slack_id = team.mentor.username.split('_')[0]
        mentor_profile = (f'https://{settings.SLACK_WORKSPACE}.slack.com/'
                          f'team/{mentor_slack_id}')
    elif team.mentor:
        mentor_profile = f'profile/{team.mentor.id}'

    return render(request, 'team.html', {
        'team': team,
        'rename_team_form': rename_team_form,
        'create_private_channel': create_private_channel,
        'mentor_profile': mentor_profile,
        'non_participant_superuser': non_participant_superuser,
        })


@login_required
@has_access_to_team()
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
@has_access_to_team()
def rename_team(request, team_id):
    """ Change the name of a HackTeam """
    hack_team = get_object_or_404(HackTeam, id=team_id)

    if (not request.user.user_type == UserType.STAFF
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
@has_access_to_team()
def create_private_channel(request, team_id):
    """ Creates a new Private Slack Channel in slack """
    slack_site_settings = SlackSiteSettings.objects.first()
    if request.method != 'POST':
        messages.error(request,
                       'You cannot access this page in this way.')
        return redirect(reverse('view_team', kwargs={'team_id': team_id}))

    team = get_object_or_404(HackTeam, id=team_id)
    non_participant_superuser = (
        (request.user.is_superuser or request.user.is_staff)
        and not request.user.is_participant(team.hackathon))

    if not (request.user in team.participants.all()
            or request.user == team.mentor or non_participant_superuser):
        messages.error(request,
                       ('You do not have access to create a Private Slack Channel '
                        'for this team.'))
        return redirect(reverse('view_team', kwargs={'team_id': team_id}))

    if (not (settings.SLACK_ENABLED or settings.SLACK_BOT_TOKEN or settings.SLACK_ADMIN_TOKEN
             or settings.SLACK_WORKSPACE) or slack_site_settings.communication_channel_type != 'slack_private_channel'):
        messages.error(request, 'This feature is currently not enabled.')
        return redirect(reverse('view_team', kwargs={'team_id': team_id}))

    # Create new channel
    date_str = datetime.now().strftime('%y%m')
    team_name = re.sub('[^A-Za-z0-9]+', '', team.display_name.lower())
    channel_name = f'{date_str}-hackathon-{team_name}'
    params = {
        'team_id': settings.SLACK_TEAM_ID,
        'name': channel_name,
        'is_private': True,
    }
    # Cannot use Bot Token to create a channel if workspace settings
    # specify only Admins and Owners can create channels 
    headers = {'Authorization': f'Bearer {settings.SLACK_ADMIN_TOKEN}'}
    create_response = requests.get(SLACK_CHANNEL_ENDPOINT, params=params,
                                   headers=headers)
    if not create_response.status_code == 200:
        messages.error(request, (f'An error occurred creating the Private Slack Channel. '
                                 f'Error code: {create_response.get("error")}'))
        return redirect(reverse('view_team', kwargs={'team_id': team_id}))
    
    create_response = create_response.json()
    if not create_response.get('ok'):
        if create_response.get('error') == 'name_taken':
            error_msg = (f'An error occurred creating the Private Slack Channel. '
                         f'A channel with the name "{channel_name}" already '
                         f'exists. Please change your team name and try again '
                         f'or contact an administrator')
        else:
            error_msg = (f'An error occurred creating the Private Slack Channel. '
                         f'Error code: {create_response.get("error")}')
        messages.error(request, error_msg)
        return redirect(reverse('view_team', kwargs={'team_id': team_id}))
    
    channel = create_response.get('channel', {}).get('id')
    communication_channel = (f'https://{settings.SLACK_WORKSPACE}.slack.com/'
                             f'app_redirect?channel={channel}')
    team.communication_channel = communication_channel
    team.save()

    pattern = re.compile(r'^U[a-zA-Z0-9]*[_]T[a-zA-Z0-9]*$')
    users = team.participants.all()
    users = [team_member.username
             for team_member in team.participants.all()]

    if team.mentor:
        users.append(team.mentor.username)

    # Add admins to channel for administration purposes
    for admin in slack_site_settings.slack_admins.all():
        users.append(admin.username)
    
    # First need to add Slack Bot to then add users to channel
    invite_bot_params = {
        'channel': channel,
        'users': settings.SLACK_BOT_ID,
    }
    response = invite_users_to_slack_channel(
        endpoint=SLACK_CHANNEL_INVITE_ENDPOINT,
        headers=headers,
        params=invite_bot_params)
    
    if not response['ok']:
        messages.error(request, response['error'])
        return redirect(reverse('view_team', kwargs={'team_id': team_id}))

    invite_team_params = {
        'channel': channel,
        'users': ','.join([user.split('_')[0]
                           for user in users if pattern.match(user)]),
    }
    headers = {'Authorization': f'Bearer {settings.SLACK_BOT_TOKEN}'}
    response = invite_users_to_slack_channel(
        endpoint=SLACK_CHANNEL_INVITE_ENDPOINT,
        headers=headers,
        params=invite_team_params)
    
    if not response['ok']:
        messages.error(request, response['error'])
        return redirect(reverse('view_team', kwargs={'team_id': team_id}))

    if len(users) < len(team.participants.all()):
        missing_users = len(team.participants.all()) - len(users)
        messages.error(request,
                       (f'Private Slack Channel successfully created, but {missing_users} '
                        f'users could not be added to the Private Slack Channel. '
                        f'Please add the missing users manually.'))
    else:
        messages.success(request, 'Private Slack Channel successfully created')

    return redirect(reverse('view_team', kwargs={'team_id': team_id}))


@login_required
@has_access_to_team()
def view_team_calendar(request, team_id):
    """ View the team calendar showing what timezone each team member is
    located at """
    hack_team = get_object_or_404(HackTeam, id=team_id)
    if (request.user not in hack_team.participants.all()
            and request.user.user_type not in [
                UserType.SUPERUSER, UserType.FACILITATOR_ADMIN,
                UserType.PARTNER_ADMIN]):
        messages.error(request, 'You do not have access to view this page')
        return redirect(reverse('view_team', kwargs={'team_id': team_id}))
    timezone = request.GET.get('timezone') or request.user.timezone
    tz = pytz.timezone(timezone)
    user_tz_offset = (datetime.now(tz).utcoffset().total_seconds()/60/60)
    headers = [{'display_name': 'Time', 'description': '',
                'timezone': timezone}]

    for member in hack_team.participants.all():
        offset = calculate_timezone_offset(member.timezone, user_tz_offset)
        quantifier = 'ahead of' if offset > 0 else 'behind'
        headers.append({
            'display_name': f'{member.slack_display_name}',
            'description': (f'{member.slack_display_name} is {abs(offset)}hrs '
                            f'{quantifier} {timezone}'),
            'timezone': member.timezone,
        })

    calendar = []
    for i in range(24):
        row = [f'{i}:00']
        for member in hack_team.participants.all():
            offset = calculate_timezone_offset(member.timezone, user_tz_offset)
            if i + offset >= 24:
                _time = (i + offset) - 24
            elif i + offset < 0:
                _time = 24 + i - abs(offset)
            else:
                _time = i + offset
            row.append(f'{int(_time)}:00')
        calendar.append(row)

    return render(request, 'team_calendar.html', {
        'hack_team': hack_team,
        'team_id': team_id,
        'redirect_url': f'/teams/{team_id}/',
        'calendar': calendar,
        'headers': headers,
        'timezones': TIMEZONE_CHOICES,
        'selected_timezone': timezone,
    })


@login_required
@has_access_to_team()
def view_team_competencies(request, team_id):
    hack_team = get_object_or_404(HackTeam, id=team_id)
    competencies = Competency.objects.filter(is_visible=True)
    redirect_url = reverse('view_team', kwargs={'team_id': team_id})
    return render(request, 'team_competencies.html', {
        'hack_team': hack_team,
        'competencies': competencies,
        'redirect_url': redirect_url,
    })
