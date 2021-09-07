import base64
import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponse, \
                        Http404
from django.shortcuts import get_object_or_404, redirect

from .helpers import image_to_base64str
from accounts.models import CustomUser
from hackathon.models import HackTeam, HackProject, Hackathon
from showcase.models import Showcase

VALID_UPLOAD_TYPES = ['profile_image', 'header_image', 'project_image',
                      'screenshot', 'hackathon_image',
                      ]


@login_required
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
            team = HackTeam.objects.get(id=upload_id)
            team.header_image = image_to_base64str(upload_file)
            team.save()
        elif upload_type == 'project_image':
            project = HackProject.objects.get(id=upload_id)
            project.project_image = image_to_base64str(upload_file)
            project.save()
        elif upload_type == 'screenshot':
            project = HackProject.objects.get(id=upload_id)
            project.screenshot = image_to_base64str(upload_file)
            project.save()
        elif upload_type == 'hackathon_image':
            hackathon = Hackathon.objects.get(id=upload_id)
            hackathon.hackathon_image = image_to_base64str(upload_file)
            hackathon.save()

        messages.success(request, 'Image uploaded successfully.')
        return redirect(request.META.get('HTTP_REFERER'))

    else:
        return HttpResponseBadRequest()


@login_required
def render_image(request, showcase_id, image_hash):
    try:
        image_hash_uuid = uuid.UUID(image_hash)
        showcase = get_object_or_404(Showcase, hash=image_hash_uuid)
        if showcase.showcase_image:
            data_uri = showcase.showcase_image
            image_data = data_uri.partition('base64,')[2]
            binary = base64.b64decode(image_data)
            return HttpResponse(binary, content_type='image/png')
    except ValueError:
        raise Http404()
    raise Http404()
