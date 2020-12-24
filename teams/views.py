from django.shortcuts import render, get_object_or_404

from hackathon.models import Hackathon, HackTeam
from teams.helpers import choose_team_sizes, group_participants,\
                          choose_team_levels, find_all_combinations,\
                          distribute_participants_to_teams


def distribute_teams(request, hackathon_id):
    """ Page that handles the logic of automatically distributing the teams
    for a hackathon and allows for the admin to re-arrange the team members """
    participants = Hackathon.objects.get(id=hackathon_id).participants.all()
    teamsize = 3
    team_sizes = sorted(choose_team_sizes(participants, teamsize))
    grouped_participants, hackathon_level = group_participants(
        participants, len(team_sizes))
    team_levels = sorted(choose_team_levels(len(team_sizes), hackathon_level))
    combos_without_dupes = find_all_combinations(
        participants, team_sizes)
    teams, leftover_participants = distribute_participants_to_teams(
        team_sizes, team_levels, grouped_participants,
        combos_without_dupes)
    # For testing only
    leftover_participants[1].append({'name': 'Tester 1', 'level': 1})
    leftover_participants[2].append({'name': 'Tester 1', 'level': 2})
    leftover_participants[3].append({'name': 'Tester 1', 'level': 3})
    leftover_participants[5].append({'name': 'Tester 1', 'level': 5})
    participants_still_to_distribute = [
        participant for participant_groups in leftover_participants.values()
        for participant in participant_groups]
    return render(request, 'distribute_teams.html',
                  {'teams': teams,
                   'leftover_participants': participants_still_to_distribute})


def view_team(request, team_id):
    """ View the detailed team information for a HackTeam """
    team = get_object_or_404(HackTeam, id=team_id)
    return render(request, 'team.html', {'team': team})
