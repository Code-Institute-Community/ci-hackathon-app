from home.models import Review
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, redirect, reverse

from .forms import PartnershipRequestForm
from .helpers import send_partnership_request_email

from hackathon.models import Hackathon, HackAward

UPCOMING_STATUSES = [
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
    partnership_form = PartnershipRequestForm()
    if not request.user.is_authenticated:
        upcoming_hackathons = Hackathon.objects.filter(
            is_public=True,
            status__in=UPCOMING_STATUSES).order_by('-start_date')

        recent_hackathons = Hackathon.objects.filter(
            is_public=True,
            status='finished',
            organisation=1).order_by('-start_date')

        winning_awards = HackAward.objects.filter(
            hack_award_category__ranking=1, hackathon__status='finished', hackathon__is_public=True
                ).order_by('-hackathon__start_date')
    else:
        if request.user.is_superuser or request.user.is_staff:
            hackathons = Hackathon.objects.exclude(
                status='deleted').order_by('-start_date')
        elif request.user.organisation:
            orgs = [1]
            orgs.append(request.user.organisation.id)
            hackathons = Hackathon.objects.filter(Q(organisation__in=orgs) | Q(is_public=True)).exclude(
                status='deleted').order_by('-start_date')
        else:
            hackathons = Hackathon.objects.filter(is_public=True).exclude(
                status='deleted').order_by('-start_date')
        
        upcoming_hackathons = Hackathon.objects.filter(
            id__in=[hackathon.id for hackathon in hackathons],
            status__in=UPCOMING_STATUSES).order_by('-start_date')

        recent_hackathons = Hackathon.objects.filter(
            id__in=[hackathon.id for hackathon in hackathons],
            status='finished').order_by('-start_date')

        winning_awards = HackAward.objects.filter(
            hackathon__id__in=[hackathon.id for hackathon in hackathons],
            hack_award_category__ranking=1, hackathon__status='finished'
                ).order_by('-hackathon__start_date')

    winning_showcases = [award.winning_project.get_showcase()
                         for award in winning_awards
                         if (award.winning_project
                             and award.winning_project.get_showcase())]
    reviews = Review.objects.filter(visible=True).order_by('-rating')

    return render(request, 'home/index.html',  {
        'recent_hackathons': recent_hackathons[:3],
        'upcoming_hackathons': upcoming_hackathons,
        'winning_showcases': winning_showcases[:3],
        'partnership_form': partnership_form,
        'reviews': reviews,
    })


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


def save_partnership_contact_form(request):
    """ Saves the requests coming from the Partnership Contact form on the
    home page """
    if request.method == 'POST':
        form = PartnershipRequestForm(request.POST)
        if form.is_valid():
            form.save()
            send_partnership_request_email(request.POST)
            messages.success(request, ("Thank you very much for your interest!"
                                       " We will be in touch shortly."))
        else:
            print(form.errors)
            messages.error(
                request, ("Sorry, there was an error submitting your request. "
                          "Please try again or send an email to "
                          f"{settings.SUPPORT_EMAIL}."))
        return redirect(reverse('home'))
    else:
        return redirect(reverse('home'))


@login_required
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


def codeofconduct(request):
    """
        A view to show the hackathon code of conduct.
    """
    return render(request, 'code-of-conduct.html')
