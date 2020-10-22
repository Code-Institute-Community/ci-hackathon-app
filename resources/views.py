from django.shortcuts import render
from .models import Resource


def resources(request):
    """ Display the useful resources and links page. """

    template = "resources/resources.html"
    resources = Resource.objects.all()

    return render(request, template, {'resources': resources})
