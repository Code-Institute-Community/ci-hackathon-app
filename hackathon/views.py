import datetime
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Hackathon, HackTeam, HackProject, HackProjectScore, HackProjectScoreCategory
from django.views.generic import ListView
from django.contrib import messages

# Create your views here.


class HackathonListView(ListView):
    """Renders a page with a list of Hackathons."""
    model = Hackathon
    ordering = ['-created']
    paginate_by = 8


@login_required
def judging(request, hack_id, team_id):
    """Displays the judging page for the judge to save their scores
    for the selected project - determined by hackathon id and team id"""

    # Becomes available only after a Hackathon End Date/Time
    
    event = Hackathon.objects.filter(pk=hack_id)
    team = HackTeam.objects.filter(pk=team_id)
    
    # verify whether user is judge for the event
    user_is_judge = False
    for judge in event.values('judges'):
        if judge['judges'] == request.user.id:
            print("judge there")
            user_is_judge = True
    if not user_is_judge:
        messages.error(request, "You are not a judge for that event!")
        template = 'hackathon/hackathon_list.html'
        return render(request, template)

    # verify if event is ready to be judged (finished)
    finish = event.values('end_date')[0]['end_date']
    now = timezone.now()
    if finish > now:
        messages.error(request, f"The event has not finished yet, check back after {finish}!")
        template = 'hackathon/hackathon_list.html'
        return render(request, template)
    print("the event has finished")

    # verify that the selected team belongs to the selected event
    team_belongs_to_event = False
    for team in event.values('teams'):
        if team['teams'] == int(team_id):
            team_belongs_to_event = True
            print("team is in event")
    if not team_belongs_to_event:
        messages.error(request, f"Nice try! That team is not part of the event...")
        template = 'hackathon/hackathon_list.html'
        return render(request, template)

    # check if the judge has already scored the requested team's Project
    
    the_event = get_object_or_404(Hackathon, pk=hack_id)
    team_ids_in_event = Hackathon.objects.filter(pk=hack_id).values_list('teams', flat=True)
    print(f"teams_in_event = {team_ids_in_event}")

    # megse kene minden team-et a templatre kuldeni, mert nehezebb kezelni ott

    teams_in_event = []
    for team in team_ids_in_event:
        teams_in_event.append(get_object_or_404(HackTeam, pk=team))
    print(f"team objects in list for the tempalte: {teams_in_event}")

    # for project in team.values('project'):
    #     print(f"Team Project: {project['project']}")

    # bar = HackProject.objects.filter(pk=project[0]['project'])
    # print(f"the project from the HackProject model: {bar}")

    # HackProjectScoreCategories for the template:
    score_categories = HackProjectScoreCategory.objects.all()

    template = 'hackathon/judging.html'
    # pass all the teams and their projects to the page, so the judge can swap
    context = {
        'hackathon': the_event,
        'teams': teams_in_event, #Project is part of the Team object
        'score_categories': score_categories,
        'selected_team': get_object_or_404(HackTeam, pk=team_id),

    }
    return render(request, template, context)
