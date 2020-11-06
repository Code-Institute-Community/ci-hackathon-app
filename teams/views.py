from django.shortcuts import render

from hackathon.models import Hackathon


def distribute_teams(request, hackathon_id):
    """ Page that handles the logic of automatically distributing the teams
    for a hackathon and allows for the admin to re-arrange the team members """
    participants = Hackathon.objects.get(id=hackathon_id)
    return render(request, "team_distribution.html",
                  {"participants": participants})
