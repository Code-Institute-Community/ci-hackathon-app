from datetime import datetime

from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.utils import timezone

from .models import Hackathon, HackTeam, HackProject, HackProjectScore, HackProjectScoreCategory
from .forms import HackathonForm


class HackathonListView(ListView):
    """Renders a page with a list of Hackathons."""
    model = Hackathon
    ordering = ["-created"]
    paginate_by = 8

    def get_context_data(self, **kwargs):
        """
        Pass in the following context to the template:
        hackathons - filter out deleted hackathons and order by newest first
        today - needed to compare dates to display delete alert for hackathons
        in progress (needed because using built in template 'now' date didn't
        work correctly for the comparison)
        """
        context = super().get_context_data(**kwargs)
        context['hackathons'] = Hackathon.objects.order_by(
            '-created').exclude(status='deleted')
        context['today'] = datetime.now()
        return context


@login_required
def judging(request, hack_id, team_id):
    """Displays the judging page for the judge to save their scores
    for the selected project - determined by hackathon id and team id"""

    # HackProjectScoreCategories:
    score_categories = HackProjectScoreCategory.objects.all()

    hackathon = get_object_or_404(Hackathon, pk=hack_id)
    team = get_object_or_404(HackTeam, pk=team_id)

    # verify whether user is judge for the hackathon
    if hackathon not in Hackathon.objects.filter(judges=request.user):
        messages.error(request, "You are not a judge for that event!")
        return render(request, 'home/index.html')

    # verify if hackathon is ready to be judged (judging_status == 'open')
    if hackathon.judging_status != 'open':
        messages.error(
            request, f"Judging is not open! {hackathon.judging_status}!")
        return render(request, 'home/index.html')

    # verify that the selected team belongs to the selected hackathon
    if team.hackathon != hackathon:
        messages.error(
            request, f"Nice try! That team is not part of the event...")
        return render(request, 'home/index.html')

    # check if the judge has already scored the requested team's Project
    project = get_object_or_404(HackTeam, pk=team_id).project
    if not project:
        messages.error(
            request, f"The team doesn't have a project yet, check back later...")
        return render(request, 'home/index.html')
    judge_has_scored_this = False
    if HackProjectScore.objects.filter(judge=request.user, project=project):
        messages.error(
            request, f"Oooops, sorry! Something went wrong, you have already scored that team...")
        return render(request, 'home/index.html')

    if request.method == 'POST':
        # judge score submitted for a team
        for score_category in score_categories:
            score_cat_id = f"score_{score_category.id}"
            team_score = HackProjectScore(
                created_by=request.user,
                judge=request.user,
                project=get_object_or_404(HackTeam, pk=team_id).project,
                score=request.POST.get(score_cat_id),
                hack_project_score_category=score_category,
            )
            team_score.save()
            check_projects_scores(hackathon, score_categories)

    context = {
        'hackathon': hackathon,
        'score_categories': score_categories,
        'team': team,
        'project': project,
    }
    return render(request, 'hackathon/judging.html', context)


def check_projects_scores(hackathon, score_categories):
    """ When a judge submits the score, check if all projects in the Hackathon
    were scored by all the judges in all the categories by comparing the number of 
    objects in HackProjectScore for each projects to the required number of objects """

    judges = hackathon.judges.count()
    number_categories = score_categories.count()
    projects = list(HackTeam.objects.filter(
        hackathon=hackathon).values_list('project', flat=True).distinct())

    # Number of objects that should be in the HackProjectScore for each project
    number_of_objects = judges * number_categories

    for project in projects:
        if HackProjectScore.objects.filter(project=project).count() == number_of_objects:
            continue
        else:
            return redirect("hackathon:hackathon-list")

    # Call a function to calculate the scores and redirect to a view that will show a list of all of the projects ranked by their score


def create_hackathon(request):
    """ Allow users to create hackathon event """

    if request.method == 'GET':
        # Redirect user if they are not admin
        if not request.user.is_superuser:
            return redirect("hackathon:hackathon-list")

        template = "hackathon/create-event.html"
        form = HackathonForm()

        return render(request, template, {"form": form})

    else:
        form = HackathonForm(request.POST)
        # Convert start and end date strings to datetime and validate
        start_date = datetime.strptime(
            request.POST.get('start_date'), '%d/%m/%Y %H:%M')
        end_date = datetime.strptime(
            request.POST.get('end_date'), '%d/%m/%Y %H:%M')
        now = datetime.now()

        # Ensure start_date is a day in the future
        if start_date.date() <= now.date():
            messages.error(
                request, 'The start date must be a date in the future.')
            return redirect("hackathon:create_hackathon")

        # Ensure end_date is after start_date
        if end_date <= start_date:
            messages.error(
                request, 'The end date must be at least one day after the start date.')
            return redirect("hackathon:create_hackathon")

        # Submit form and save record
        if form.is_valid():
            form.instance.created_by = request.user
            form.save()
            messages.success(
                request, 'Thanks for submitting a new Hackathon event!')
        return redirect("hackathon:hackathon-list-scores")


@login_required
def update_hackathon(request, hackathon_id):
    """ Allow users to edit hackathon event """

    # Redirect user if they are not admin
    if not request.user.is_superuser:
        return redirect("hackathon:hackathon-list")

    hackathon = get_object_or_404(Hackathon, pk=hackathon_id)
    if request.method == 'GET':
        form = HackathonForm(instance=hackathon)

        context = {
            "form": form,
            "hackathon_id": hackathon_id,
        }

        return render(request, "hackathon/create-event.html", context)

    else:
        form = HackathonForm(request.POST, instance=hackathon)
        # Convert start and end date strings to datetime and validate
        start_date = datetime.strptime(
            request.POST.get('start_date'), '%d/%m/%Y %H:%M')
        end_date = datetime.strptime(
            request.POST.get('end_date'), '%d/%m/%Y %H:%M')
        now = datetime.now()

        # Ensure start_date is a day in the future for hackathons that haven't started yet
        if hackathon.start_date.date() > now.date() >= start_date.date():
            messages.error(
                request, 'The start date must be a date in the future.')
            return redirect("hackathon:update_hackathon", hackathon_id)

        # Ensure end_date is after start_date
        if end_date <= start_date:
            messages.error(
                request, 'The end date must be at least one day after the start date.')
            return redirect("hackathon:update_hackathon", hackathon_id)

        # Submit form and save record
        if form.is_valid():
            form.instance.updated = now
            form.save()
            messages.success(
                request, f'Thanks, {hackathon.display_name} has been successfully updated!')
        return redirect("hackathon:hackathon-list")


@login_required
def delete_hackathon(request, hackathon_id):
    """ Allow users to 'soft delete' hackathon event - set status to 'deleted'
     to remove from frontend list """

    # Redirect user if they are not admin
    if not request.user.is_superuser:
        return redirect("hackathon:hackathon-list")

    # Get selected hackathon and set status to deleted to remove from frontend list
    hackathon = get_object_or_404(Hackathon, pk=hackathon_id)
    hackathon.status = 'deleted'
    hackathon.save()

    messages.success(
        request, f'{hackathon.display_name} has been successfully deleted!')
    return redirect("hackathon:hackathon-list")

class HackathonDetailView(DetailView):
    """Renders a page with Hackathon details."""
    model = Hackathon
    context_object_name = "hackathon"


def enroll_toggle(request):
    user = request.user
    data = {}
    if request.method == "POST":

        # Gets the PK of the Hackathon and then the related Hackathon
        hackathon_id = request.POST.get("hackathon-id")
        hackathon = Hackathon.objects.get(pk=hackathon_id)

        if user.is_staff:
            if user in hackathon.judges.all():
                hackathon.judges.remove(user)
                data["message"] = "You have withdrawn from judging."
            else:
                hackathon.judges.add(user)
                data["message"] = "You have enrolled as a judge."
        
        else:
            if user in hackathon.participants.all():
                hackathon.participants.remove(user)
                data["message"] = "You have withdrawn from this Hackaton."
            else:
                hackathon.participants.add(user)
                data["message"] = "You have enrolled successfully."

        data["tag"] = "Success"
        return JsonResponse(data)

    else:
        return HttpResponse(status=403)
