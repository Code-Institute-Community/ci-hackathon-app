from functools import wraps

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import reverse, redirect

from accounts.models import UserType


def can_access(allowed_types, redirect_url=None, redirect_kwargs={}):
    def decorator(view_function):
        @wraps(view_function)
        def wrapped_view(request, *args, **kwargs):
            print(request.user.user_type)
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
