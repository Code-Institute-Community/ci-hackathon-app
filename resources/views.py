
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, get_object_or_404

from .forms import ResourceForm
from .models import Resource
from accounts.decorators import can_access
from accounts.models import UserType


def resources(request):
    """ Display the useful resources and links page. """
    template = "resources/resources.html"
    resources = Resource.objects.all()

    return render(request, template, {'resources': resources})


@login_required
@can_access([UserType.SUPERUSER, UserType.STAFF, UserType.FACILITATOR_ADMIN,
             UserType.PARTNER_ADMIN],
            redirect_url='resources')
def add_resource(request):
    """ A view allowing admin to add a resource to the resources page """
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added resource!')
            return redirect(reverse('resources'))
        else:
            messages.error(request, 'Failed to add resource. Please ensure the form is valid.')  # noqa: E501
    else:
        ResourceForm()

    template = 'resources/add_resource.html'

    return render(request, template, {'form': ResourceForm()})


@login_required
@can_access([UserType.SUPERUSER, UserType.STAFF, UserType.FACILITATOR_ADMIN,
             UserType.PARTNER_ADMIN],
            redirect_url='resources')
def delete_resource(request, resource_id):
    """ A view to allow only admin to delete a resource """
    resource = get_object_or_404(Resource, pk=resource_id)
    resource.delete()
    messages.info(request, f'{resource.name} was successfully deleted.')
    return redirect(reverse('resources'))


@login_required
@can_access([UserType.SUPERUSER, UserType.STAFF, UserType.FACILITATOR_ADMIN,
             UserType.PARTNER_ADMIN],
            redirect_url='resources')
def edit_resource(request, resource_id):
    """ A view to allow only admin to edit a resource"""
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


