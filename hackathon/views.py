from django.shortcuts import render
from django.views.generic import ListView

from .models import Hackathon


class HackathonListView(ListView):
    """Renders a page with a list of Hackathons."""
    model = Hackathon
    context_object_name = 'hackathons'
    ordering = ['-created']
    paginate_by = 10
