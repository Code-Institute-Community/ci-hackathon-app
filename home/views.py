from django.shortcuts import render, redirect, reverse

from hackathon.models import Hackathon


def index(request):
    """ The view to be redirected to after login which will check if the
    user's full name is present, if it is not redirect to edit profile,
    otherwise redirect to home
    """
    if request.user.full_name:
        return redirect(reverse('home'))

    return redirect(reverse('edit_profile'))


def home(request):
    """ 
    A view to return the index page
    and upcoming Hackathon information
    """
    hackathons = Hackathon.objects.all()

    return render(request, "home/index.html",  {"hackathons": hackathons})


def faq(request):
    """ A view to return the FAQ page """

    return render(request, "faq.html")


def judging_criteria(request):
    """ A view to return the Judging Criteria page """

    return render(request, "judging-criteria.html")


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