from django.shortcuts import render

from hackathon.models import Hackathon


def index(request):
    """ 
    A view to return the index page
    and upcoming Hackathon information
    """
    hackathons = Hackathon.objects.all()

    context = {
        'hackathons': hackathons,
    }

    return render(request, "home/index.html", context)


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

