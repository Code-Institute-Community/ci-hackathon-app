from datetime import datetime

from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Hackathon
from .forms import HackathonForm


class HackathonListView(ListView):
    """Renders a page with a list of Hackathons."""
    model = Hackathon
    ordering = ['-created']
    paginate_by = 8


@login_required
def create_hackathon(request):
    """ Allow users to create hackathon event """

    if request.method == 'GET':
        # Redirect user if they are not admin
        if not request.user.is_superuser:
            return redirect("hackathon:hackathon-list")

        template = "hackathon/create-event.html"
        form = HackathonForm()

        return render(request, template, {"form": form})

    else:
        form = HackathonForm(request.POST)
        # Convert start and end date strings to datetime and validate
        start_date = datetime.strptime(request.POST.get('start_date'), '%d/%m/%Y %H:%M')
        end_date = datetime.strptime(request.POST.get('end_date'), '%d/%m/%Y %H:%M')
        now = datetime.now()

        # Ensure start_date is a day in the future
        if start_date.date() <= now.date():
            messages.error(request, 'The start date must be a date in the future.')
            return redirect("hackathon:create_hackathon")

        # Ensure end_date is after start_date
        if end_date <= start_date:
            messages.error(request, 'The end date must be at least one day after the start date.')
            return redirect("hackathon:create_hackathon")

        # Submit form and save record
        if form.is_valid():
            form.instance.created_by = request.user
            form.save()
            messages.success(request, 'Thanks for submitting a new Hackathon event!')
        return redirect("hackathon:hackathon-list")

    pass
