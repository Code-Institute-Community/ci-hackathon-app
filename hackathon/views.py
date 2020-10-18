from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def create_event(request):
    """ Allow users to create hackathon event """

    template = "hackathon/create-event.html"
    context = {}

    return render(request, template, context)
