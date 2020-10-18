from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Hackathon, HackTeam, HackProject, HackProjectScore, HackProjectScoreCategory

# Create your views here.

@login_required
def judging(request):
    """Displays the judging landing page for the judge to save their scores
    for each submitted project"""

    
    template = 'hackathon/judging.html'
    context = {}
    return render(request, template, context)