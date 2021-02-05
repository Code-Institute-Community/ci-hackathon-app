from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.models import CustomUser


@login_required
def profile(request, user_id=None):
    """ Display the user's profile. """
    context = {
        'is_owner': True,
    }
    
    if user_id is not None:
        user = get_object_or_404(CustomUser, id=user_id)
        # If the user's org is CI then anybody can see them
        # If the user is in the same or as the request.user they can see them
        # Or if the request.user is staff they can see them
        if (user.organisation == 1 
                or user.organisation == request.user.organisation
                or request.user.is_staff):
            context['user'] = user
        else:
            context['user'] = None
        context['is_owner'] = False

    template = "profiles/profile.html"
    return render(request, template, context)
