from copy import deepcopy
from datetime import datetime
from operator import itemgetter

from dateutil.parser import parse
from django.forms import modelformset_factory
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.utils import timezone

from .models import Hackathon, HackTeam, HackProject, HackProjectScore, HackProjectScoreCategory, HackAwardCategory
from .forms import HackathonForm, ChangeHackathonStatusForm,\
                   HackAwardCategoryForm
from .lists import AWARD_CATEGORIES

DEFAULT_SCORES = {
    'team_name': '',
    'project_name': '',
    'scores': {},
    'total_score': 0,
}


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
        return redirect(reverse('home'))

    # verify if hackathon is ready to be judged
    if hackathon.status not in ['hack_in_progress', 'judging']:
        messages.error(
            request, f"Judging is not open! {hackathon.status}!")
        return redirect(reverse('home'))

    # verify that the selected team belongs to the selected hackathon
    if team.hackathon != hackathon:
        messages.error(
            request, f"Nice try! That team is not part of the event...")
        return redirect(reverse('home'))

    # check if the judge has already scored the requested team's Project
    project = get_object_or_404(HackTeam, pk=team_id).project
    if not project:
        messages.error(
            request, f"The team doesn't have a project yet, check back later...")
        return redirect(reverse('home'))
    judge_has_scored_this = False
    if HackProjectScore.objects.filter(judge=request.user, project=project):
        messages.error(
            request, f"Oooops, sorry! Something went wrong, you have already scored that team...")
        return redirect(reverse('home'))

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
        return redirect(reverse('hackathon:view_hackathon',
                                kwargs={'hackathon_id': hack_id}))

    context = {
        'hackathon': hackathon,
        'score_categories': score_categories,
        'team': team,
        'project': project,
    }
    return render(request, 'hackathon/judging.html', context)


@login_required
def check_projects_scores(request, hack_id):
    """ When a judge submits the score, check if all projects in the Hackathon
    were scored by all the judges in all the categories by comparing the number of 
    objects in HackProjectScore for each projects to the required number of objects.

    If all projects weren't scored, render final_score.html without the score table.

    If all the projects were scored, calculate the total score for each team, sort the teams by scores
    and render final_score.html with the score table.

    """
    hackathon = get_object_or_404(Hackathon, pk=hack_id)
    HackAwardCategoryFormSet = modelformset_factory(
                HackAwardCategory, fields=('id', 'display_name', 'winning_project'),
                form=HackAwardCategoryForm, extra=0)

    if request.method == 'POST':
        hack_awards_formset = HackAwardCategoryFormSet(
            request.POST,
            queryset=HackAwardCategory.objects.filter(hackathon=hackathon))
        if hack_awards_formset.is_valid():
            hack_awards_formset.save()
        else:
            print(hack_awards_formset.errors)
            pass
        return redirect(reverse('hackathon:final_score', kwargs={'hack_id': hack_id}))

    else:
        team_scores = {}
        category_scores_per_team = {}
        score_categories = HackProjectScoreCategory.objects.all()
        hackathon_projects = [team.project.id for team in hackathon.teams.all()
                              if team.project]
        scores = HackProjectScore.objects.filter(
            project_id__in=hackathon_projects).all()
        judges = hackathon.judges.all()

        # Creating scores data structure
        # {
        #   team_name: {
        #       team_name: 'Team',
        #       project_name: 'Project',
        #       scores: {
        #           judge_1: {
        #               'Score Category 1': 1,
        #               ...
        #               'Score Category n': 1,
        #               'Total': 2
        #           },
        #           judge_n: {
        #               ...
        #           }
        #       },
        #       total_score: 5
        #   }
        # }
        for score in scores:
            judge_name = score.judge.slack_display_name
            team_name = score.project.hackteam.display_name
            project_name = score.project.display_name
            score_category = score.hack_project_score_category.category
            team_scores.setdefault(team_name, deepcopy(DEFAULT_SCORES))
            team_scores[team_name]['team_name'] = team_name
            team_scores[team_name]['project_name'] = project_name
            team_scores[team_name]['scores'].setdefault(judge_name, {})
            team_scores[team_name]['scores'][judge_name].setdefault('Total', 0)
            team_scores[team_name]['scores'][judge_name][score_category] = (
                score.score)
            team_scores[team_name]['total_score'] += score.score
            team_scores[team_name]['scores'][judge_name][
                'Total'] += score.score

            category_scores_per_team.setdefault(score_category, {})
            category_scores_per_team[score_category].setdefault(team_name, 0)
            category_scores_per_team[score_category][team_name] += score.score
        
        # Fill empty totals for any judges who have not submitted scores
        for team, team_score in team_scores.items():
            for judge in judges:
                if judge.slack_display_name not in team_score['scores']:
                    team_score['scores'][judge.slack_display_name] = {
                        'Total': 0}

        sorted_team_scores = sorted(team_scores.values(),
                                    key=itemgetter('total_score'),
                                    reverse=True)

        # Ordering scores per category
        category_scores_per_category = {}
        for category, scores in category_scores_per_team.items():
            category_scores_per_category[category] = sorted(
                [{"team_name": team_name, "score": score}
                 for team_name, score in scores.items()],
                key=itemgetter('score'),
                reverse=True)
        
        # Grouping back into teams
        category_scores = {team.display_name : {} for team in hackathon.teams.all()}
        for category, teams in category_scores_per_category.items():
            max_score = max([team['score'] for team in teams])
            place = 1
            for team in teams:
                category_scores[team['team_name']].setdefault(category, {})
                category_scores[team['team_name']][category]['score'] = team['score']
                if team['score'] < max_score:
                    place += 1
                category_scores[team['team_name']][category]['place'] = place

        hack_awards_formset = HackAwardCategoryFormSet(
            queryset=HackAwardCategory.objects.filter(hackathon=hackathon))

        return render(request, 'hackathon/final_score.html', {
            'sorted_teams_scores': sorted_team_scores,
            'category_scores': category_scores,
            'hackathon': hackathon.display_name,
            'judges': judges,
            'hack_awards_formset': hack_awards_formset,
        })


def create_hackathon(request):
    """ Allow users to create hackathon event """

    if request.method == 'GET':
        # Redirect user if they are not admin
        if not request.user.is_superuser:
            return redirect("hackathon:hackathon-list")

        template = "hackathon/create-event.html"
        form = HackathonForm(initial={
            'organisation': 1,
            'score_categories':HackProjectScoreCategory.objects.all()[:5]})

        return render(request, template, {"form": form})

    else:
        form = HackathonForm(request.POST)
        # Convert start and end date strings to datetime and validate
        start_date = parse(request.POST.get('start_date'))
        end_date = parse(request.POST.get('end_date'))
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
            form.instance.organiser = request.user
            form.save()
            # Taking the first 3 award categories and creating them for the
            # newly created hackathon
            for award_category in AWARD_CATEGORIES[:3]:
                hack_award = HackAwardCategory.objects.filter(
                    display_name=award_category).first()
                if not hack_award:
                    continue
                hack_award.pk = None
                hack_award.created_by = request.user
                hack_award.hackathon = form.instance
                hack_award.save()
            messages.success(
                request, 'Thanks for submitting a new Hackathon event!')
        return redirect("hackathon:hackathon-list")


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
        start_date = parse(request.POST.get('start_date'))
        end_date = parse(request.POST.get('end_date'))
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
            # saved_form = form.save(commit=False)
            # saved_form.save()
            # form.save_m2m()
            messages.success(
                request, f'Thanks, {hackathon.display_name} has been successfully updated!')
        return redirect("hackathon:hackathon-list")


@login_required
def update_hackathon_status(request, hackathon_id):
    # Redirect user if they are not admin
    if not request.user.is_superuser:
        return redirect("hackathon:hackathon-list")
    
    if request.method == 'POST':
        hackathon = get_object_or_404(Hackathon, id=hackathon_id)
        hackathon.status = request.POST.get('status')
        hackathon.save()
        messages.success(request, 'Hackathon status updated successfully.')
        return redirect(reverse('hackathon:view_hackathon',
                                kwargs={'hackathon_id': hackathon_id}))
    else:
        return redirect("hackathon:hackathon-list") 


@login_required
def view_hackathon(request, hackathon_id):
    """
    Login required decorator used to prevent user from navigating using URL
    injection or by using browser back button etc, by redirecting user to
    login page.

    Render Hackathon details and teams registered for same.

    If teams count > 3 show pagination for teams.
    """
    hackathon = get_object_or_404(Hackathon, pk=hackathon_id)

    teams = HackTeam.objects.filter(hackathon_id=hackathon_id).order_by(
        'display_name')
    paginator = Paginator(teams, 3)
    page = request.GET.get('page')
    paged_teams = paginator.get_page(page)

    context = {
        'hackathon': hackathon,
        'teams': paged_teams,
        'change_status_form': ChangeHackathonStatusForm(instance=hackathon),
    }

    return render(request, "hackathon/hackathon_view.html", context)


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


@login_required
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
                messages.success(request, "You have withdrawn from judging.")
            else:
                hackathon.judges.add(user)
                messages.success(request, "You have enrolled as a judge.")
        else:
            if user in hackathon.participants.all():
                hackathon.participants.remove(user)
                messages.success(request,
                                 "You have withdrawn from this Hackaton.")
            else:
                hackathon.participants.add(user)
                messages.success(request, "You have enrolled successfully.")
        return redirect(reverse('hackathon:view_hackathon',
                                kwargs={'hackathon_id': hackathon_id}))
    else:
        return HttpResponse(status=403)


# @login_required
# def update_hack_awards(request):
#     if request.method == 'POST':
#         pass
#     else:
#         HackAwardCategoryFormSet = modelformset_factory(
#             HackAwardCategory, fields=('display_name', 'project'),
#             formset=HackAwardCategoryFormSet)