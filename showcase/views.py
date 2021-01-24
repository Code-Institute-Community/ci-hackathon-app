import random

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import render, reverse, redirect, get_object_or_404

from .forms import ShowcaseForm
from .models import Showcase
from hackathon.models import HackTeam, HackProject
from images.helpers import image_to_base64str

SHOWCASE_SPOTLIGHT_NUMBER = settings.SHOWCASE_SPOTLIGHT_NUMBER 


def view_showcases(request):
    """ Shows the project showcase page """
    all_showcases = Showcase.objects.order_by('display_name')
    print(all_showcases)
    print(SHOWCASE_SPOTLIGHT_NUMBER)
    top_results = Showcase.objects.all().order_by('?')[
        :SHOWCASE_SPOTLIGHT_NUMBER]
    print(top_results)
    return render(request, 'showcase.html', {
        'top_results': top_results,
        'all_showcases': all_showcases,
    })


def view_showcase(request, showcase_id):
    """ View the detailed team information for a Showcase """
    showcase = get_object_or_404(Showcase, id=showcase_id)
    if not showcase.is_public:
        response = render(request, '404.html')
        response.status_code = 404
        return response

    team = showcase.get_team()
    anon_members = range(len(team.participants.all())
                         - len(showcase.showcase_participants.all()))

    return render(request, 'team.html', {
        'team': team,
        'showcase': showcase,
        'anon_members': anon_members,
        })


@login_required
def create_or_update_showcase(request, team_id):
    """ Creates or updates the project showcase entry """
    team = get_object_or_404(HackTeam, id=team_id)
    showcase = team.project.get_showcase()

    if request.method == 'GET':
        if showcase:
            form = ShowcaseForm(team_id=team_id, instance=showcase)
        else:
            form = ShowcaseForm(team_id=team_id, initial={"hack_project": 1})
    else:
        data = request.POST
        image = request.FILES.get('image')

        if showcase:
            form = ShowcaseForm(data, team_id=team_id, instance=showcase)
        else:
            form = ShowcaseForm(data, team_id=team_id)

        if form.is_valid():
            if image:
                f = form.save(commit=False)
                f.showcase_image = image_to_base64str(image)
                f.save()
                form.save_m2m()
            else:
                form.save()

            return redirect(reverse('create_or_update_showcase',
                                    kwargs={'team_id': team_id}))
        else:
            return redirect(reverse('create_or_update_showcase',
                                    kwargs={'team_id': team_id}))

    return render(request, 'edit_showcase.html', {
        'form': form,
        'project': team.project,
        'showcase_image': showcase.showcase_image if showcase else None
    })
