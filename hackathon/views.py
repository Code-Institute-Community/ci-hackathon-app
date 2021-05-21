from copy import deepcopy
from datetime import datetime
import logging

from django.db import transaction, IntegrityError
from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse

from .models import Hackathon, HackTeam, HackProject, HackProjectScore,\
                    HackProjectScoreCategory, HackAwardCategory, HackAward
from .forms import HackathonForm, ChangeHackathonStatusForm,\
                   HackAwardForm
from .lists import AWARD_CATEGORIES
from .helpers import format_date, query_scores, create_judges_scores_table

from accounts.models import UserType
from accounts.decorators import can_access

DEFAULT_SCORES = {
    'team_name': '',
    'project_name': '',
    'scores': {},
    'total_score': 0,
}

logger = logging.getLogger(__name__)


@login_required
def list_hackathons(request):
    """ Lists all hackathons available to a given student

        TODO: Fix permissions as below
        EXTERNAL_USER should only see Hackathons set to `is_public=True`
        Any PARTNER_* users should see all hackathons where the oranisation
        is the same as the user's and all public hackathons
        Any other user should see all CI hackathons and all public hackathons
        SUPERUSER and STAFF should see all hackathons

    """
    if request.user.user_type == UserType.EXTERNAL_USER:
        hackathons = Hackathon.objects.filter(is_public=True).order_by(
        '-created').exclude(status='deleted')
    elif request.user.user_type in [UserType.PARTNER_ADMIN,
            UserType.PARTNER_JUDGE, UserType.PARTNER_USER]:
        hackathons = Hackathon.objects.filter(
            organisation=request.user.organisation).order_by('-created'
            ).exclude(status='deleted')
    else:
        hackathons = Hackathon.objects.order_by('-created').exclude(
            status='deleted')
    paginator = Paginator(hackathons, 8)
    page = request.GET.get('page')
    paged_hackathons = paginator.get_page(page)

    return render(request, 'hackathon/hackathon_list.html', {
        'hackathons': paged_hackathons,
        'today': datetime.now(),
    })


@login_required
@can_access([UserType.SUPERUSER, UserType.STAFF, UserType.FACILITATOR_ADMIN,
             UserType.FACILITATOR_JUDGE, UserType.PARTNER_ADMIN,
             UserType.PARTNER_JUDGE],
             redirect_url='hackathon:hackathon-list')
def judging(request, hackathon_id, team_id):
    """Displays the judging page for the judge to save their scores
    for the selected project - determined by hackathon id and team id"""
    hackathon = get_object_or_404(Hackathon, pk=hackathon_id)
    score_categories = HackProjectScoreCategory.objects.filter(
        category__in=list(hackathon.score_categories.all())).all()
    team = get_object_or_404(HackTeam, pk=team_id)

    if request.method == 'POST':
        # judge score submitted for a team
        for score_category in score_categories:
            team_score = HackProjectScore.objects.filter(
                judge=request.user,
                project=get_object_or_404(HackTeam, pk=team_id).project,
                hack_project_score_category=score_category,
            )

            score_cat_id = f"score_{score_category.id}"
            if team_score:
                team_score.update(score=request.POST.get(score_cat_id))   
            else:
                team_score = HackProjectScore(
                    created_by=request.user,
                    judge=request.user,
                    project=get_object_or_404(HackTeam, pk=team_id).project,
                    score=request.POST.get(score_cat_id),
                    hack_project_score_category=score_category,
                )
                team_score.save()

        if request.POST.get('redirect_url'):
            return redirect(reverse(request.POST.get('redirect_url'),
                                kwargs={'hackathon_id': hackathon_id}))

        return redirect(reverse('hackathon:view_hackathon',
                                kwargs={'hackathon_id': hackathon_id}))
    else:
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
                request, ("The team doesn't have a project yet, check back "
                          "later..."))
            return redirect(reverse('home'))

        scores = {
            score.hack_project_score_category.category: score.score
            for score in HackProjectScore.objects.filter(
                judge=request.user, project=project)
        }

        redirect_url = request.GET.get('next') or ''

        context = {
            'hackathon': hackathon,
            'score_categories': score_categories,
            'team': team,
            'project': project,
            'existing_scores': scores or {},
            'redirect_url': redirect_url,
        }
        return render(request, 'hackathon/judging.html', context)


@login_required
@can_access([UserType.SUPERUSER, UserType.FACILITATOR_ADMIN,
             UserType.PARTNER_ADMIN], redirect_url='hackathon:hackathon-list')
def check_projects_scores(request, hackathon_id):
    """ When a judge submits the score, check if all projects in the Hackathon
    were scored by all the judges in all the categories by comparing the
    number of objects in HackProjectScore for each projects to the required
    number of objects.

    If all projects weren't scored, render final_score.html without the
    score table.

    If all the projects were scored, calculate the total score for each team,
    sort the teams by scores
    and render final_score.html with the score table.

    """
    hackathon = get_object_or_404(Hackathon, pk=hackathon_id)
    HackAwardFormSet = modelformset_factory(
                HackAward, fields=('id', 'hack_award_category',
                                   'winning_project'),
                form=HackAwardForm, extra=0)

    if request.method == 'POST':
        hack_awards_formset = HackAwardFormSet(
            request.POST,
            form_kwargs={'hackathon_id': hackathon_id},
            queryset=HackAward.objects.filter(hackathon=hackathon))
        if hack_awards_formset.is_valid():
            try:
                with transaction.atomic():
                    hack_awards_formset.save()
            except IntegrityError as e:
                if 'UNIQUE' in str(e):
                    messages.error(request, 
                                   ("Each award category can only be added "
                                    "once to a hackathon."))
                else: 
                    logger.exception(e)
                    messages.error(request, 
                                   ("An unexpected error occurred. Please "
                                    "try again."))
        else:
            messages.error(request, 
                           "An unexpected error occurred. Please try again.")
        return redirect(reverse('hackathon:final_score',
                                kwargs={'hackathon_id': hackathon_id}))

    else:
        judges = [judge.slack_display_name for judge in hackathon.judges.all()]
        teams  = [team.display_name for team in hackathon.teams.all()
                  if team.project]
        scores = query_scores(hackathon_id)
        scores_table = create_judges_scores_table(scores, judges, teams)

        hack_awards_formset = HackAwardFormSet(
            form_kwargs={'hackathon_id': hackathon_id},
            queryset=HackAward.objects.filter(hackathon=hackathon))

        return render(request, 'hackathon/final_score.html', {
            'hackathon': hackathon.display_name,
            'hack_awards_formset': hack_awards_formset,
            'scores_table': scores_table,
            'teams_without_projects': '\n'+'\n'.join([
                team.display_name
                for team in hackathon.teams.all()
                if not team.project]),
        })


@login_required
@can_access([UserType.SUPERUSER, UserType.FACILITATOR_ADMIN,
             UserType.PARTNER_ADMIN], redirect_url='hackathon:hackathon-list')
def create_hackathon(request):
    """ Allow users to create hackathon event """
    if request.method == 'GET':
        template = "hackathon/create-event.html"
        form = HackathonForm(initial={
            'organisation': 1,
            'team_size': 3,
            'score_categories':HackProjectScoreCategory.objects.all()[:5]})

        return render(request, template, {"form": form})

    else:
        form = HackathonForm(request.POST)
        # Convert start and end date strings to datetime and validate
        start_date = format_date(request.POST.get('start_date'))
        end_date = format_date(request.POST.get('end_date'))
        now = datetime.now()
        # Ensure start_date is a day in the future
        if start_date.date() <= now.date():
            messages.error(
                request, 'The start date must be a date in the future.')
            return redirect("hackathon:create_hackathon")

        # Ensure end_date is after start_date
        if end_date <= start_date:
            messages.error(
                request, ('The end date must be at least one day after the '
                         'start date.'))
            return redirect("hackathon:create_hackathon")

        # Submit form and save record
        if form.is_valid():
            form.instance.created_by = request.user
            form.instance.organiser = request.user
            form.save()
            # Taking the first 3 award categories and creating them for the
            # newly created hackathon.
            hack_award_categories = HackAwardCategory.objects.filter(
                display_name__in=AWARD_CATEGORIES[:3])
            for award_category in hack_award_categories:
                hack_award = HackAward(
                    created_by = request.user,
                    hackathon = form.instance,
                    hack_award_category=award_category,
                )
                hack_award.save()
            messages.success(
                request, 'Thanks for submitting a new Hackathon event!')
        else:
            messages.error(request, ("An error occurred creating the event. "
                                     "Please try again."))
        return redirect("hackathon:hackathon-list")


@login_required
@can_access([UserType.SUPERUSER, UserType.FACILITATOR_ADMIN,
             UserType.PARTNER_ADMIN], redirect_url='hackathon:hackathon-list')
def update_hackathon(request, hackathon_id):
    """ Allow users to edit hackathon event """
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

        start_date = format_date(request.POST.get('start_date'))
        end_date = format_date(request.POST.get('end_date'))
        now = datetime.now()

        # Ensure start_date is a day in the future for hackathons that haven't
        # started yet
        if hackathon.start_date.date() > now.date() >= start_date.date():
            messages.error(
                request, 'The start date must be a date in the future.')
            return redirect("hackathon:update_hackathon", hackathon_id)

        # Ensure end_date is after start_date
        if end_date <= start_date:
            messages.error(
                request, ('The end date must be at least one day after the '
                         'start date.'))
            return redirect("hackathon:update_hackathon", hackathon_id)

        # Submit form and save record
        if form.is_valid():
            form.instance.updated = now
            form.save()
            messages.success(
                request, (f'Thanks, {hackathon.display_name} has been '
                          f'successfully updated!'))
        else:
            messages.error(request, ("An error occurred updating the event. "
                                     "Please try again."))
        return redirect("hackathon:hackathon-list")


@login_required
@can_access([UserType.SUPERUSER, UserType.FACILITATOR_ADMIN,
             UserType.PARTNER_ADMIN], redirect_url='hackathon:hackathon-list')
def update_hackathon_status(request, hackathon_id):
    """ Allows users to updated the status of a hackathon """
    if request.method == 'POST':
        hackathon = get_object_or_404(Hackathon, id=hackathon_id)
        hackathon.status = request.POST.get('status')
        hackathon.save()
        messages.success(request, 'Hackathon status updated successfully.')
        return redirect(reverse('hackathon:view_hackathon',
                                kwargs={'hackathon_id': hackathon_id}))
    else:
        messages.error(request, ("An error occurred updating the event "
                                 "status. Please try again."))
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
    # TODO: Add check if the user has access to this specific hackathon based
    # on the user_type (e.g. external and partner hackathons)
    hackathon = get_object_or_404(Hackathon, pk=hackathon_id)
    teams = HackTeam.objects.filter(hackathon_id=hackathon_id).order_by(
        'display_name')
    paginator = Paginator(teams, 3)
    page = request.GET.get('page')
    paged_teams = paginator.get_page(page)
    create_group_im = (settings.SLACK_ENABLED and settings.SLACK_BOT_TOKEN)


    context = {
        'hackathon': hackathon,
        'teams': paged_teams,
        'change_status_form': ChangeHackathonStatusForm(instance=hackathon),
        'create_group_im': create_group_im,
    }

    return render(request, "hackathon/hackathon_view.html", context)


@login_required
@can_access([UserType.SUPERUSER, UserType.FACILITATOR_ADMIN,
             UserType.PARTNER_ADMIN], redirect_url='hackathon:hackathon-list')
def delete_hackathon(request, hackathon_id):
    """ Allow users to 'soft delete' hackathon event - set status to 'deleted'
     to remove from frontend list """

    # Get selected hackathon and set status to deleted to remove from
    # frontend list
    hackathon = get_object_or_404(Hackathon, pk=hackathon_id)
    hackathon.status = 'deleted'
    hackathon.save()

    messages.success(
        request, f'{hackathon.display_name} has been successfully deleted!')
    return redirect("hackathon:hackathon-list")


@login_required
def enroll_toggle(request):
    user = request.user
    data = {}
    if request.method == "POST":
        # Gets the PK of the Hackathon and then the related Hackathon
        hackathon_id = request.POST.get("hackathon-id")
        hackathon = Hackathon.objects.get(pk=hackathon_id)
        if user.user_type == UserType.STAFF:
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


@login_required
@can_access([UserType.SUPERUSER, UserType.FACILITATOR_ADMIN,
             UserType.PARTNER_ADMIN], redirect_url='hackathon:hackathon-list')
def change_awards(request, hackathon_id):
    hackathon = get_object_or_404(Hackathon, pk=hackathon_id)
    awards = hackathon.awards.all()

    if request.method == 'GET':
        form = HackAwardForm()
        return render(request, 'hackathon/change_awards.html', {
            'hackathon': hackathon,
            'awards': awards,
            'form': form,
        })
    else: 
        if request.POST.get('update_type') == 'delete':
            hack_award = get_object_or_404(HackAward,
                                           id=request.POST.get('id'))
            if hack_award.winning_project:
                messages.error(request,
                               ("You cannot remove this award since it already"
                               " has a winner assigned to it."))
                return redirect(reverse('hackathon:awards',
                                kwargs={'hackathon_id': hackathon_id}))
            hack_award.delete()
            messages.success(request, "Award removed added.")
        else:
            form = HackAwardForm(request.POST)
            existing_awards = HackAward.objects.filter(
                hackathon=hackathon,
                hack_award_category__in=request.POST.get(
                    'hack_award_category')).all()

            if existing_awards:
                messages.error(request, ("Each award category can only be "
                                         "added once to a hackathon."))
            elif form.is_valid():
                f = form.save(commit=False)
                f.created_by = request.user
                f.hackathon = hackathon
                form.save()
                messages.success(request, "Award successfully added.")
            else:
                logger.exception(form.errors)
                messages.error(request,
                               "An unexpected error occurred. Please try again")
        return redirect(reverse('hackathon:awards',
                                kwargs={'hackathon_id': hackathon_id}))


@login_required
@can_access([UserType.SUPERUSER, UserType.STAFF, UserType.FACILITATOR_ADMIN,
             UserType.FACILITATOR_JUDGE, UserType.PARTNER_ADMIN,
             UserType.PARTNER_JUDGE],
             redirect_url='hackathon:hackathon-list')
def judge_teams(request, hackathon_id):
    """ Shows the list of teams and allows a judge to go to the scoring
    page """
    hackathon = get_object_or_404(Hackathon, id=hackathon_id)

    if hackathon not in Hackathon.objects.filter(judges=request.user):
        messages.error(request, "You are not a judge for that event!")
        return redirect(reverse('home'))

    return render(request, 'hackathon/judge_teams.html', {
        'teams': hackathon.teams,
    })
