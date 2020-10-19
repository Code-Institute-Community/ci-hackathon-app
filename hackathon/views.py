from django.views.generic import ListView, DetailView

from .models import Hackathon


class HackathonListView(ListView):
    """Renders a page with a list of Hackathons."""
    model = Hackathon
    ordering = ['-created']
    paginate_by = 8


class HackathonDetailView(DetailView):
    """Renders a page with Hackathon details."""
    model = Hackathon
    context_object_name = 'hackathon'
