from django.views.generic import ListView, DetailView
from django.http import JsonResponse, HttpResponse

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
    # Checks to make sure the user has the permissions to enroll
    user = request.user
    data = {}
    if (request.method == "POST") and (user.is_staff):

        # Gets the PK of the Hackathon and then the related Hackathon
        hackathon_id = request.POST.get("hackathon-id")
        hackathon = Hackathon.objects.get(pk=hackathon_id)

        # Either enrolls or unenrolls a user from the judges
        if user in hackathon.judges.all():
            hackathon.judges.remove(user)
            data['message'] = "You have withdrawn from judging."
        else:
            hackathon.judges.add(user)
            data['message'] = "You have enrolled a judge."

        data["tag"] = "success"
        data["id"] = hackathon_id
        return JsonResponse(data)
    else:
        return HttpResponse(status=403)
