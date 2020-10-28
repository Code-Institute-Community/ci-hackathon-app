from datetime import datetime
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Hackathon, HackTeam, HackProject, HackProjectScore, HackProjectScoreCategory
from .forms import HackathonForm

# Create your views here.

class HackathonListView(ListView):
    """Renders a page with a list of Hackathons."""
    model = Hackathon
    ordering = ['-created']
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
        context['hackathons'] = Hackathon.objects.order_by('-created').exclude(status='deleted')
        context['today'] = datetime.now()
        return context


@login_required
def judging(request, hack_id, team_id):
    """Displays the judging page for the judge to save their scores
    for the selected project - determined by hackathon id and team id"""

    # HackProjectScoreCategories:
    score_categories = HackProjectScoreCategory.objects.all()

    event = Hackathon.objects.filter(pk=hack_id)
    team = HackTeam.objects.filter(pk=team_id)

    # verify whether user is judge for the event
    user_is_judge = False
    for judge in event.values('judges'):
        if judge['judges'] == request.user.id:
            user_is_judge = True
    if not user_is_judge:
        messages.error(request, "You are not a judge for that event!")
        template = 'home/index.html'
        return render(request, template)

    # verify if event is ready to be judged (finished)
    finish = event.values('end_date')[0]['end_date']
    now = timezone.now()
    if finish > now:
        messages.error(request, f"The event has not finished yet, check back after {finish}!")
        template = 'home/index.html'
        return render(request, template)

    # verify that the selected team belongs to the selected event
    team_belongs_to_event = False
    for team in event.values('teams'):
        if team['teams'] == int(team_id):
            team_belongs_to_event = True
    if not team_belongs_to_event:
        messages.error(request, f"Nice try! That team is not part of the event...")
        template = 'home/index.html'
        return render(request, template)

    # check if the judge has already scored the requested team's Project
    the_event = get_object_or_404(Hackathon, pk=hack_id)
    project = get_object_or_404(HackTeam, pk=team_id).project
    judge_has_scored_this = False
    if HackProjectScore.objects.filter(judge=request.user, project=project):
        messages.error(request, f"Oooops, sorry! Something went wrong, you have already scored that team...")
        template = 'home/index.html'
        return render(request, template)
    
    if request.method == 'POST':
        # judge score submitted for a team
        for score_category in score_categories:
            score_cat_id = f"score_{score_category.id}"
            team_score = HackProjectScore(
                created_by = request.user,
                judge = request.user,
                project = get_object_or_404(HackTeam, pk=team_id).project,
                score = request.POST.get(score_cat_id),
                hack_project_score_category = score_category,
            )
            team_score.save()
            
        return redirect("hackathon:hackathon-list")

    selected_team = get_object_or_404(HackTeam, pk=team_id)
    selected_project = get_object_or_404(HackProject, pk=selected_team.project.id)

    template = 'hackathon/judging.html'
    context = {
        'hackathon': the_event,
        'score_categories': score_categories,
        'team': selected_team,
        'project': selected_project,
    }
    return render(request, template, context)


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
        start_date = datetime.strptime(request.POST.get('start_date'), '%d/%m/%Y %H:%M')
        end_date = datetime.strptime(request.POST.get('end_date'), '%d/%m/%Y %H:%M')
        now = datetime.now()

        # Ensure start_date is a day in the future
        if start_date.date() <= now.date():
            messages.error(request, 'The start date must be a date in the future.')
            return redirect("hackathon:create_hackathon")

        # Ensure end_date is after start_date
        if end_date <= start_date:
            messages.error(request, 'The end date must be at least one day after the start date.')
            return redirect("hackathon:create_hackathon")

        # Submit form and save record
        if form.is_valid():
            form.instance.created_by = request.user
            form.save()
            messages.success(request, 'Thanks for submitting a new Hackathon event!')
        return redirect("hackathon:hackathon-list")

    pass


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

    messages.success(request, f'{hackathon.display_name} has been successfully deleted!')
    return redirect("hackathon:hackathon-list")
