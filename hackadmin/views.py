from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from hackathon.models import Hackathon


@login_required
def hackadmin_panel(request):
    """ Used for admin to view all registered users and allows to filter
    by individual hackathon """
    if not request.user.is_superuser:
        messages.error(request, 'You do not have access to this page.')
        return reverse(reverse('hackathon:hackathon-list'))

    hackathons = Hackathon.objects.all().exclude(status='deleted')
    users = get_user_model().objects.all()
    return render(request, 'hackathon/hackathon_stats.html', {
        'hackathons': hackathons,
        'users': users,
    })

@login_required
def hackathon_stats(request):
    """ Used for admin to view all registered users and allows to filter
    by individual hackathon """
    if not request.user.is_superuser:
        messages.error(request, 'You do not have access to this page.')
        return reverse(reverse('hackathon:hackathon-list'))

    hackathons = Hackathon.objects.all().exclude(status='deleted')
    users = get_user_model().objects.all()
    return render(request, 'hackathon/hackathon_stats.html', {
        'hackathons': hackathons,
        'users': users,
    })
