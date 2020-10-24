from django.shortcuts import render, redirect, reverse
from .models import Resource
from django.contrib import messages
from .forms import ResourceForm
from django.contrib.auth.decorators import login_required



def resources(request):
    """ Display the useful resources and links page. """

    template = "resources/resources.html"
    resources = Resource.objects.all()

    return render(request, template, {'resources': resources})


@login_required
def add_resource(request):
    """ A view allowing admin to add a resource to the resources page """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only admin can add resources.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save()
            messages.success(request, 'Successfully added resource!')
            return redirect(reverse('resources'))
        else:
            messages.error(request, 'Failed to add resource. Please ensure the form is valid.')
    else:
        form = ResourceForm()

    template = 'resources/add_resource.html'

    return render(request, template, {'form': form})