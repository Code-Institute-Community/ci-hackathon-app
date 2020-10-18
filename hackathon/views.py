from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Hackathon, HackAwardCategory, HackTeam, HackProject, HackProjectScore, HackProjectScoreCategory
from .forms import HackathonForm


@login_required
def create_event(request):
    """ Allow users to create hackathon event """

    if request.method == 'GET':
        # TODO: Add conditional to check if user is admin - if not, redirect to Hackathon events list
        # TODO: Incorporate editing event in the same view in GET conditional:
        #  - Get pk from params (passed in when user clicks 'EDIT' in events list
        #  - If pk, get object and form instance and pass in as form context to enable pre-rendering data in frontend
        #  - Else, pass empty form in as form context to frontend

        template = "hackathon/create-event.html"
        form = HackathonForm()
        context = {
            "form": form,
        }

        return render(request, template, context)

    if request.method == 'POST':
        pass

    pass
