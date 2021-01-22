from django.shortcuts import render


def showcase(request):
    """ Shows the project showcase page """
    return render(request, 'showcase.html')
