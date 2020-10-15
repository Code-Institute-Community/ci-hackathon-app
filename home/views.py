from django.shortcuts import render


def index(request):
    """ A view to return the index page """

    return render(request, "home/index.html")

def criteria(request):
    """ A view to return the judging criteria page """

    return render(request, "home/criteria.html")
