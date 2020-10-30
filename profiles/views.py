from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    """ Display the user's profile. """
    # to do - help wanted

    template = "profiles/profile.html"
    context = {}

    return render(request, template, context)