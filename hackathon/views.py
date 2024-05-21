from datetime import datetime
import logging
import calendar

from django.db import transaction, IntegrityError
from django.forms import modelformset_factory
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.views.generic import ListView
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder

from .models import Hackathon, HackTeam, HackProjectScore,\
                    HackProjectScoreCategory, HackAwardCategory, HackAward, Event
from .forms import HackathonForm, ChangeHackathonStatusForm,\
                   HackAwardForm, HackTeamForm
from .lists import AWARD_CATEGORIES
from .helpers import format_date, query_scores, create_judges_scores_table
from .tasks import send_email_from_template

from accounts.models import UserType
from accounts.decorators import can_access, has_access_to_hackathon

#Calendar for hackathon
import calendar
from django.shortcuts import render

DEFAULT_SCORES = {
    'team_name': '',
    'project_name': '',
    'scores': {},
    'total_score': 0,
}

logger = logging.getLogger(__name__)


def list_hackathons(request):
    """ Lists all hackathons available to a given student """
    if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
        hackathons = Hackathon.objects.exclude(
            status='deleted').order_by('-start_date')
    elif request.user.is_authenticated and request.user.organisation:
        orgs = [1]
        orgs.append(request.user.organisation.id)
        hackathons = Hackathon.objects.filter(Q(organisation__in=orgs) | Q(is_public=True)).exclude(
            status='deleted').order_by('-start_date')
    else:
        hackathons = Hackathon.objects.filter(is_public=True).exclude(
            status='deleted').order_by('-start_date')

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
                request, "Nice try! That team is not part of the event...")
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
        teams = [team.display_name for team in hackathon.teams.all()
                 if team.project]
        scores = query_scores(hackathon_id)
        scores_table = create_judges_scores_table(scores, judges, teams)

        hack_awards_formset = HackAwardFormSet(
            form_kwargs={'hackathon_id': hackathon_id},
            queryset=hackathon.awards.all())

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
            'is_public': True,
            'score_categories': HackProjectScoreCategory.objects.filter(
                is_active=True)[:5]})

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
            hackathon_name = form.instance.display_name
            # Create the event in the calendar for the intro webinar
            intro_webinar_date = form.cleaned_data.get('intro_webinar_date')
            presentations_webinar_date = form.cleaned_data.get('presentations_date')
            Event.objects.create(
                    title=f'{hackathon_name} Intro Webinar',
                    start=intro_webinar_date,
                    body=f'The intro webinar for the {hackathon_name} hackathon',
                )
            Event.objects.create(
                    title=f'{hackathon_name} Presentations Webinar',
                    start=presentations_webinar_date,
                    body=f'The project presentations webinar for the {hackathon_name} hackathon',
                )
            form.save()
            # Taking the first 3 award categories and creating them for the
            # newly created hackathon.
            hack_award_categories = HackAwardCategory.objects.filter(
                display_name__in=AWARD_CATEGORIES[:3])
            for award_category in hack_award_categories:
                hack_award = HackAward(
                    created_by=request.user,
                    hackathon=form.instance,
                    hack_award_category=award_category,
                )
                hack_award.save()
            messages.success(
                request, 'Thanks for submitting a new Hackathon event!')
        else:
            logger.exception(form.errors)
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
@has_access_to_hackathon()
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
    create_private_channel = (settings.SLACK_ENABLED and settings.SLACK_BOT_TOKEN
                              and settings.SLACK_ADMIN_TOKEN)

    context = {
        'hackathon': hackathon,
        'teams': paged_teams,
        'change_status_form': ChangeHackathonStatusForm(instance=hackathon),
        'create_private_channel': create_private_channel,
    }

    return render(request, "hackathon/hackathon_view.html", context)


def view_hackathon_public(request, hackathon_id):
    """ A limited view of the hackathon page for the public """
    hackathon = get_object_or_404(Hackathon, pk=hackathon_id)
    redirect_url = (request.META.get('HTTP_REFERER') or reverse('home'))
    if hackathon.status == 'deleted':
        messages.error(request, 'This hackathon does not exist.')
        return redirect(redirect_url)

    return render(request, "hackathon/hackathon_view_public.html", {
        'hackathon': hackathon})


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
@has_access_to_hackathon()
def enroll_toggle(request):
    if request.method == "POST":
        judge_user_types = [
            UserType.SUPERUSER, UserType.STAFF, UserType.FACILITATOR_ADMIN,
            UserType.FACILITATOR_JUDGE, UserType.PARTNER_ADMIN,
            UserType.PARTNER_JUDGE,
        ]
        hackathon = get_object_or_404(Hackathon,
                                      id=request.POST.get("hackathon-id"))
        if request.user in hackathon.judges.all():
            hackathon.judges.remove(request.user)
            send_email_from_template.apply_async(args=[request.user.email, request.user.first_name, hackathon.display_name, 'withdraw_judge'])
            messages.success(request, "You have withdrawn from judging.")
        elif request.user in hackathon.participants.all():
            hackathon.participants.remove(request.user)
            send_email_from_template.apply_async(args=[request.user.email, request.user.first_name, hackathon.display_name, 'withdraw_participant'])
            messages.success(request,
                             "You have withdrawn from this Hackaton.")
        elif (request.POST.get('enrollment-type') == 'judge'
                and request.user.user_type in judge_user_types):
            hackathon.judges.add(request.user)
            send_email_from_template.apply_async(args=[request.user.email, request.user.first_name, hackathon.display_name, 'enroll_judge'])
            messages.success(request, "You have enrolled as a facilitator/judge.")  # noqa: E501
        else:
            if hackathon.max_participants_reached():
                messages.error(request,
                               "Sorry, but the registration is closed.")
                return redirect(reverse('hackathon:view_hackathon', kwargs={
                    'hackathon_id': request.POST.get("hackathon-id")}))
            hackathon.participants.add(request.user)
            send_email_from_template.apply_async(args=[request.user.email, request.user.first_name, hackathon.display_name, 'enroll_participant'])
            messages.success(request, "You have enrolled successfully.")

        return redirect(reverse(
            'hackathon:view_hackathon',
            kwargs={'hackathon_id': request.POST.get("hackathon-id")}))
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
                messages.error(
                    request, "An unexpected error occurred. Please try again")
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
        'hackathon': hackathon,
        'teams': hackathon.teams,
    })


@login_required
@can_access([UserType.SUPERUSER, UserType.FACILITATOR_ADMIN,
             UserType.PARTNER_ADMIN], redirect_url='hackathon:hackathon-list')
def assign_mentors(request, hackathon_id):
    """ View used to assign a mentor to each team """
    hackathon = get_object_or_404(Hackathon, id=hackathon_id)
    HackMentorFormSet = modelformset_factory(
        HackTeam, fields=('id', 'display_name', 'mentor'),
        form=HackTeamForm, extra=0)

    if request.method == 'GET':
        hack_mentors_formset = HackMentorFormSet(
            form_kwargs={'hackathon_id': hackathon_id},
            queryset=HackTeam.objects.filter(hackathon=hackathon))

        return render(request, 'hackathon/assign_mentors.html', {
            'hackathon': hackathon,
            'hack_mentors_formset': hack_mentors_formset,
        })
    else:
        hack_mentors_formset = HackMentorFormSet(
            request.POST,
            form_kwargs={'hackathon_id': hackathon_id},
            queryset=HackTeam.objects.filter(hackathon=hackathon))

        if hack_mentors_formset.is_valid():
            hack_mentors_formset.save()
            messages.success(request, "Facilitators updated successfully!")
            return redirect(reverse('hackathon:assign_mentors',
                                    kwargs={'hackathon_id': hackathon_id}))
        else:
            messages.error(request,
                           (f"An unexpected error occurred: "
                            f"{hack_mentors_formset.errors}"))


def event_list(request):
    """ 
    Get a list of events for the calendar from the events db
    """
    event_list_data = Event.objects.all()
    event_list = [{
        'id': str(event.id),
        'calendarId': event.calendar_id,
        'title': event.title,
        'category': event.category,
        'body': event.body,
        'start': event.start.strftime('%Y-%m-%dT%H:%M:%S'),
        'end': event.end.strftime('%Y-%m-%dT%H:%M:%S'),
    } for event in event_list_data]
    return JsonResponse(event_list, safe=False, encoder=DjangoJSONEncoder)
