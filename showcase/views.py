import random

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import render, reverse, redirect, get_object_or_404

from .forms import ShowcaseForm
from .models import Showcase, ShowcaseSiteSettings
from hackathon.models import HackTeam, HackProject
from images.helpers import image_to_base64str

SHOWCASE_SPOTLIGHT_NUMBER = settings.SHOWCASE_SPOTLIGHT_NUMBER 


def view_showcases(request):
    """ Shows the project showcase page """
    showcase_settings = ShowcaseSiteSettings.objects.first()
    showcase_hackathons = showcase_settings.hackathons.all()
    featured_hackathons = showcase_settings.featured_hackathons.all()

    showcase_hackathons_teams = [team.id
                                 for hackathon in showcase_hackathons
                                 for team in hackathon.teams.all()]
    showcase_featured_hackathons_teams = [
        team.id for featured_hackathon in featured_hackathons
        for team in featured_hackathon.teams.all()]

    all_showcases = Showcase.objects.filter(
        hack_project__hackteam__in=showcase_hackathons_teams,
        is_public=True
    ).order_by('display_name')

    top_results = Showcase.objects.filter(
        hack_project__hackteam__in=showcase_featured_hackathons_teams,
        is_public=True
    ).order_by('?')[:SHOWCASE_SPOTLIGHT_NUMBER]

    paginator = Paginator(all_showcases, 5)
    page = request.GET.get('page')
    paginated_showcases = paginator.get_page(page)
    
    return render(request, 'showcase.html', {
        'top_results': top_results,
        'all_showcases': paginated_showcases,
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
        'rename_team_form': None,
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
            form = ShowcaseForm(team_id=team_id, 
                                initial={"hack_project": team.project.id})
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
                f.created_by = request.user
                f.save()
                form.save_m2m()
            else:
                f = form.save(commit=False)
                f.created_by = request.user
                f.save()
                form.save_m2m()
            
            messages.success(request, "Project showcase created successfully.")
            return redirect(reverse('create_or_update_showcase',
                                    kwargs={'team_id': team_id}))
        else:
            messages.error(request, ("An error occurred creating the project "
                                     "showcase. Please try again."))
            return redirect(reverse('create_or_update_showcase',
                                    kwargs={'team_id': team_id}))

    return render(request, 'edit_showcase.html', {
        'form': form,
        'project': team.project,
        'showcase_image': showcase.showcase_image if showcase else None
    })
