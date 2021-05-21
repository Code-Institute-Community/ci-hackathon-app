from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, reverse, redirect

from accounts.models import UserType
from accounts.decorators import can_access
from hackathon.models import Hackathon


@login_required
@can_access([UserType.SUPERUSER, UserType.STAFF, UserType.FACILITATOR_ADMIN],
            redirect_url='hackathon:hackathon-list')
def hackadmin_panel(request):
    """ Used for admin to view all registered users and allows to filter
    by individual hackathon """

    hackathons = Hackathon.objects.all().exclude(status='deleted')
    users = get_user_model().objects.all()
    return render(request, 'hackathon_stats.html', {
        'hackathons': hackathons,
        'users': users,
    })


@login_required
@can_access([UserType.SUPERUSER, UserType.STAFF, UserType.FACILITATOR_ADMIN],
            redirect_url='hackathon:hackathon-list')
def hackathon_stats(request):
    """ Used for admin to view all registered users and allows to filter
    by individual hackathon """

    hackathons = Hackathon.objects.all().exclude(status='deleted')
    users = get_user_model().objects.all()
    return render(request, 'hackathon_stats.html', {
        'hackathons': hackathons,
        'users': users,
    })
