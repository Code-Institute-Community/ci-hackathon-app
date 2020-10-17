from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.contrib.auth.models import User
from .forms import ExtendedSignupForm


@receiver(user_signed_up)
def user_signed_up(request, user, **kwargs):
    user.is_active = False
    user.save()
