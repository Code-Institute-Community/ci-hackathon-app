from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings
from django.shortcuts import render, redirect, reverse

from hackathon.models import Hackathon

PUBLIC_STATUSES = [
    'published', 'registration_open', 'hack_prep', 'hack_in_progress',
    'judging'
]


def index(request):
    """ The view to be redirected to after login which will check if the
    user's full name is present, if it is not redirect to edit profile,
    otherwise redirect to home
    """
    if not request.user.current_lms_module:
        messages.warning(request, 'Please fill in your profile.')
        return redirect(reverse('edit_profile'))
    
    return redirect(reverse('home'))


def home(request):
    """ 
    A view to return the index page and upcoming Hackathon information 
    for any public hackathons (e.g. future and ongoing with CI as organisation)
    """
    hackathons = Hackathon.objects.filter(
        status__in=PUBLIC_STATUSES,
        organisation=1).order_by('id')
    paginator = Paginator(hackathons, 2)
    page = request.GET.get('page')
    paged_hackathons = paginator.get_page(page)

    return render(request, "home/index.html",  {"hackathons": paged_hackathons})


def faq(request):
    """ A view to return the FAQ page """
    support_email = settings.SUPPORT_EMAIL

    return render(request, "faq.html", {'support_email': support_email})


def plagiarism_policy(request):
    """ A view to return the Plagiarism Policy page """

    return render(request, "plagiarism-policy.html")


def privacy_policy(request):
    """ A view to return the Privacy Policy page """

    return render(request, "privacy-policy.html")


def useful_resources(request):
    """ A view to return the Useful Resources page """

    return render(request, "useful-resources.html")


def test_500(request):
    response = render(request, '500.html')
    response.status_code = 500
    return response


def test_404(request):
    response = render(request, '404.html')
    response.status_code = 404
    return response
