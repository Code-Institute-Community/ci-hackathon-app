from django.contrib import messages
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.core.files.images import ImageFile
from django.core.files.base import ContentFile

from .helpers import image_to_base64str
from accounts.models import CustomUser
from hackathon.models import HackTeam, HackProject

VALID_UPLOAD_TYPES = ['profile_image', 'header_image', 'project_image']


def save_image(request):
    """ Receives a form with an image converts it to base64 and saves it to
    the right model based on upload_type """
    if request.method == 'POST':
        if not request.FILES:
            messages.error(request, 'No image selected.')
            return redirect(request.META.get('HTTP_REFERER'))

        data = request.POST
        upload_type = data['image-upload-type']
        upload_file = request.FILES['image']
        upload_id = data['image-upload-identifier']

        if upload_type not in VALID_UPLOAD_TYPES:
            messages.error(request, 'Wrong upload type used.')
            return redirect(request.META.get('HTTP_REFERER'))
        
        if upload_type == 'profile_image':
            user = CustomUser.objects.get(id=request.user.id)
            user.profile_image = image_to_base64str(upload_file)
            user.save()
        elif upload_type == 'header_image':
            print(upload_id)
            team = HackTeam.objects.get(id=upload_id)
            team.header_image = image_to_base64str(upload_file)
            team.save()
        elif upload_type == 'project_image':
            project = HackProject.objects.get(id=upload_id)
            project.project_image = image_to_base64str(upload_file)
            project.save()

        messages.success(request, 'Image uploaded successfully.')
        return redirect(request.META.get('HTTP_REFERER'))
        
    else:
        return HttpResponseBadRequest()
    return redirect(request.META.get('HTTP_REFERER'))

