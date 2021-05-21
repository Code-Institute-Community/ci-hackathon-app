from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, reverse, redirect, get_object_or_404

from accounts.models import UserType
from accounts.decorators import can_access
from hackathon.models import Hackathon


@login_required
@can_access([UserType.SUPERUSER, UserType.STAFF, UserType.FACILITATOR_ADMIN,
             UserType.PARTNER_ADMIN],
            redirect_url='hackathon:hackathon-list')
def hackadmin_panel(request):
    """ Used for admin to view all registered users and allows to filter
    by individual hackathon """
    # TODO: Filter hackathons by user type, PARTNER_ADMIN should not have
    # access to all hackathons and users
    hackathons = Hackathon.objects.order_by('-start_date').exclude(
        status='deleted')
    return render(request, 'hackadmin_panel.html', {
        'hackathons': hackathons,
    })


@login_required
@can_access([UserType.SUPERUSER, UserType.STAFF, UserType.FACILITATOR_ADMIN,
             UserType.PARTNER_ADMIN],
            redirect_url='hackathon:hackathon-list')
def hackathon_participants(request, hackathon_id):
    """ Used for admin to view all registered users and allows to filter
    by individual hackathon """
    # TODO: Filter hackathons by user type, PARTNER_ADMIN should not have
    # access to all hackathons and users
    slack_url = None
    hackathon = get_object_or_404(Hackathon, id=hackathon_id)
    mentors = [{   
        'team': team,
        'mentor': team.mentor 
        } for team in hackathon.teams.all()]
    if settings.SLACK_ENABLED:
        slack_url = f'https://{settings.SLACK_WORKSPACE}.slack.com/team/'
    return render(request, 'hackadmin_participants.html', {
        'hackathon': hackathon,
        'mentors': mentors,
        'slack_url': slack_url,
    })


@login_required
@can_access([UserType.SUPERUSER, UserType.STAFF, UserType.FACILITATOR_ADMIN,
             UserType.PARTNER_ADMIN],
            redirect_url='hackathon:hackathon-list')
def all_users(request):
    """ Used for admin to view all registered users and allows to filter
    by individual hackathon """
    # TODO: Filter hackathons by user type, PARTNER_ADMIN should not have
    # access to all hackathons and users
    hackathons = Hackathon.objects.all().exclude(status='deleted')
    users = get_user_model().objects.all()
    return render(request, 'all_users.html', {
        'hackathons': hackathons,
        'users': users,
    })
