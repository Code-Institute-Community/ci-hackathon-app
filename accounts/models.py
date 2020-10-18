from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.contrib.auth.models import User


@receiver(user_signed_up)
def user_signed_up(request, user, **kwargs):
    # capture server request object in dict for easy accessing of headers within
    form = dict(request.POST)
    print(form)
    # check user_type value for explicit statement and set user active
    # permission to true/false
    if form['user_type'][0] == 'participant':
        user.is_active = True
    elif form['user_type'][0] == 'staff':
        user.is_active = False
        user.is_staff = True
    else:
        user.is_active = False
        user.is_staff = True
        user.is_superuser = True
    user.save()
