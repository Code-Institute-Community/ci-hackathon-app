import datetime
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Hackathon, HackTeam, HackProject, HackProjectScore, HackProjectScoreCategory
from django.views.generic import ListView

# Create your views here.


class HackathonListView(ListView):
    """Renders a page with a list of Hackathons."""
    model = Hackathon
    ordering = ['-created']
    paginate_by = 8


@login_required
def judging(request, hack_id, team_id):
    """Displays the judging page for the judge to save their scores
    for the selected project - determined by hackathon id and team id"""

    # Becomes available only after a Hackathon End Date/Time
    
    events = Hackathon.objects.all()
    open_events = []
    for hackathon in events:
        start = hackathon.start_date
        finish = hackathon.end_date
        now = timezone.now()
        if start < now and now < finish:
            open_events.append(hackathon)
    number_of_open_events = len(open_events)
    print(f"There is/are {number_of_open_events} open event(s) atm, \nthey are: {open_events}")

    # Users can see this page, but only judges should be able to start the judging process
    judging_events = Hackathon.objects.filter(judges=request.user)
    print(f"hackathons filterd for the user as judge: {judging_events}")

    template = 'hackathon/judging.html'
    context = {
        'number_of_open_events': number_of_open_events,
        'open_events': open_events,
        'judging_events': judging_events,
        'number_of_events_to_judge': len(judging_events),
    }
    return render(request, template, context)
