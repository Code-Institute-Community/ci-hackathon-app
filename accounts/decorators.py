from functools import wraps

from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import reverse, redirect

from accounts.models import UserType
from hackathon.models import Hackathon, HackTeam


def can_access(allowed_types, redirect_url=None, redirect_kwargs={}):
    def decorator(view_function):
        @wraps(view_function)
        def wrapped_view(request, *args, **kwargs):
            authorized = (request.user.user_type in allowed_types
                          or request.user.user_type is UserType.SUPERUSER)

            if not authorized and redirect_url:
                messages.error(request, 'You do not have access to this page!')
                return redirect(reverse(redirect_url, kwargs=redirect_kwargs))
            elif not authorized:
                raise PermissionDenied('You do not have access to this page!')

            return view_function(request, *args, **kwargs)

        return wrapped_view

    return decorator


def has_access_to_hackathon(redirect_url=None, redirect_kwargs={}):
    def decorator(view_function):
        @wraps(view_function)
        def wrapped_view(request, *args, **kwargs):
            if request.user.is_superuser or request.user.is_staff:
                return view_function(request, *args, **kwargs)

            hackathon_id = kwargs.get('hackathon_id') or request.POST.get('hackathon-id')
            hackathon = get_object_or_404(Hackathon, id=hackathon_id)
            if (hackathon.organisation.id != 1
                    and hackathon.organisation.id != request.user.organisation.id
                    and hackathon.is_public is False):
                messages.error(request, 'You cannot access this page.')
                return redirect(reverse('hackathon:hackathon-list'))

            return view_function(request, *args, **kwargs)

        return wrapped_view

    return decorator


def has_access_to_team(redirect_url=None, redirect_kwargs={}):
    def decorator(view_function):
        @wraps(view_function)
        def wrapped_view(request, *args, **kwargs):
            if request.user.is_superuser or request.user.is_staff:
                return view_function(request, *args, **kwargs)

            team_id = kwargs.get('team_id')
            team = get_object_or_404(HackTeam, id=team_id)
            if not team.hackathon:
                messages.error(request, 'You cannot access this page.')
                return redirect(reverse('hackathon:hackathon-list'))

            if (team.hackathon.organisation.id != 1
                    and team.hackathon.organisation.id != request.user.organisation.id
                    and team.hackathon.is_public is False):
                messages.error(request, 'You cannot access this page.')
                return redirect(reverse('hackathon:hackathon-list'))

            return view_function(request, *args, **kwargs)

        return wrapped_view

    return decorator