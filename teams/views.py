from django.shortcuts import render

from hackathon.models import Hackathon


def distribute_teams(request, hackathon_id):
    """ Page that handles the logic of automatically distributing the teams
    for a hackathon and allows for the admin to re-arrange the team members """
    participants = Hackathon.objects.get(id=hackathon_id).participants.all()
    teamsize = 3
    num_teams = len(participants) / teamsize
    # distribute(participants, teamsize, num_teams)

    return render(request, "distribute_teams.html",
                  {"participants": participants})
