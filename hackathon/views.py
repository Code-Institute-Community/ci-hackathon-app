from django.views.generic import ListView, DetailView
from django.http import HttpResponse

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


def ajax_enroll_toggle(request):
    """Swaps between being enrolled as a judge and unenrolling."""
    if request.method == "POST":
        status = HttpResponse.status_code
    return HttpResponse(status=204)
