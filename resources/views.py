from django.shortcuts import render


def resources(request):
    """ Display the useful resources and links page. """

    template = "resources/resources.html"
    context = {}

    return render(request, template, context)
