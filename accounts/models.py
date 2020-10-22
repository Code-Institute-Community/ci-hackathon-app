from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.db.models.signals import post_delete
from allauth.account.signals import user_signed_up

from .lists import USER_TYPES_CHOICES, LMS_MODULES_CHOICES
import logging

# Initialise instance of a logger to handle error logging
logger = logging.getLogger(__name__)


class Organisation(models.Model):
    display_name = models.CharField(
        max_length=100,
        default='Code Institute',
        blank=True
    )

    def __str__(self):
        return self.display_name


class Profile(models.Model):
    """
    Define Profile Model with OneToOne relationship to AUTH_USER_MODEL and
    custom fields to suit Signup Form Extending in forms.py replicating same
    in DB.
    Using "related_name" in the OneToOne relationship between the two models
    specifies the reverse relationship to the User Model, allowing us to
    target the custom fields for injection into the profile.html
    template via `{{ user.profile.<<field_name>> }}`.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, default=1,
        related_name='profile',
        on_delete=models.CASCADE
    )
    slack_display_name = models.CharField(
        max_length=80,
        blank=False,
        default=''
    )
    user_type = models.CharField(
        max_length=20,
        blank=False,
        default='',
        choices=USER_TYPES_CHOICES
    )
    current_lms_module = models.CharField(
        max_length=35,
        blank=False,
        default='',
        choices=LMS_MODULES_CHOICES
    )
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name='profile',
        blank=True
    )

    def save(self, *args, **kwargs):
        # when signup takes place
        try:
            self.slack_display_name = self.user.slack_display_name
            self.user_type = self.user.user_type
            self.current_lms_module = self.user.current_lms_module
            self.organisation = self.user.organisation
        # when saving via admin panel
        except KeyError:
            self.slack_display_name = self.user.profile.slack_display_name
            self.user_type = self.user.profile.user_type
            self.current_lms_module = self.user.profile.current_lms_module
            self.organisation = self.user.profile.organisation
            logger.exception(str(KeyError))
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        """
        Return Class object to string via the user email value
        """
        return self.user.email


@receiver(user_signed_up)
def user_signed_up(request, user, **kwargs):
    """
    Capture server request object in dict from QueryDict, to access form values.

    Iterate over user_type field value to check for type and set permissions
    based on user story and save user to User and Profile Models.
    """
    form = dict(request.POST)

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

    # Save linked instance of user object to profile model
    Profile.objects.create(user=user)


@receiver(post_delete, sender=Profile)
def post_delete_user(sender, instance, *args, **kwargs):
    """
    admin - delete user at same time as profile deletion
    """
    if instance:
        instance.user.delete()


