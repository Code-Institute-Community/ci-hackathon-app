from django.shortcuts import render, redirect, reverse, get_object_or_404
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
        form = ResourceForm(request.POST)
        if form.is_valid():
            resource = form.save()
            messages.success(request, 'Successfully added resource!')
            return redirect(reverse('resources'))
        else:
            messages.error(request, 'Failed to add resource. Please ensure the form is valid.')
    else:
        ResourceForm()

    template = 'resources/add_resource.html'

    return render(request, template, {'form': ResourceForm()})


@login_required
def delete_resource(request, resource_id):
    """ A view to allow only admin to delete a resource """
    if not request.user.is_superuser:
        messages.error(request, 'Access denied!\
            Only admin can delete resources.')
        return redirect(reverse('home'))
    resource = get_object_or_404(Resource, pk=resource_id)
    resource.delete()
    messages.info(request, f'{resource.name} was successfully deleted.')
    return redirect(reverse('resources'))


@login_required
def edit_resource(request, resource_id):
    """ A view to allow only admin to edit a resource"""
    if not request.user.is_superuser:
        messages.error(request, 'Access denied!\
             Only admin can edit resources.')
        return redirect(reverse('home'))
    resource = get_object_or_404(Resource, pk=resource_id)
    if request.method == 'POST':
        form = ResourceForm(request.POST, instance=resource)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated resource!')
            return redirect(reverse('resources'))
        else:
            messages.error(request, 'Failed to update resource.\
                 Please ensure the form is valid.')
    else:
        ResourceForm(instance=resource)

    template = 'resources/edit_resource.html'
    context = {
        'form': ResourceForm(instance=resource),
        'resource': resource,
    }

    return render(request, template, context)