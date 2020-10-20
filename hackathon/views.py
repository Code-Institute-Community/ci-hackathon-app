from django.views.generic import ListView, DetailView
from django.http import JsonResponse

from .models import Hackathon


class HackathonListView(ListView):
    """Renders a page with a list of Hackathons."""
    model = Hackathon
    ordering = ["-created"]
    paginate_by = 8


class HackathonDetailView(DetailView):
    """Renders a page with Hackathon details."""
    model = Hackathon
    context_object_name = "hackathon"


def ajax_enroll_toggle(request):
    """Swaps between being enrolled as a judge and unenrolling."""
    if request.method == "POST":
        hackathon_id = request.POST.get("hackathon-id")
        data = {"id": hackathon_id}
        return JsonResponse(data)
