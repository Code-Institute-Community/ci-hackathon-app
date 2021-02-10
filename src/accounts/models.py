from django.db import models
from django.contrib.auth.models import AbstractUser

from .lists import USER_TYPES_CHOICES, LMS_MODULES_CHOICES
from teams.lists import LMS_LEVELS


class Organisation(models.Model):
    DEFAULT_PK = 1
    display_name = models.CharField(
        max_length=100,
        default='Code Institute'
    )

    def __str__(self):
        return self.display_name


class CustomUser(AbstractUser):
    """ Custom user model extending the basic AbstractUser model """

    full_name = models.CharField(
        max_length=255,
        blank=False,
        default=''
    )

    slack_display_name = models.CharField(
        max_length=80,
        blank=False,
        default=''
    )

    user_type = models.CharField(
        max_length=20,
        blank=False,
        default='participant',
        choices=USER_TYPES_CHOICES
    )

    current_lms_module = models.CharField(
        max_length=50,
        blank=False,
        default='',
        choices=LMS_MODULES_CHOICES
    )

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name='users',
        default=1
    )

    about = models.TextField(
        default='',
        help_text=('A short description of yourself')
    )

    website_url = models.URLField(
        max_length=255,
        blank=False,
        default='',
        help_text=('Website, GitHub or Linkedin URL')
    )

    profile_image = models.TextField(
        default='',
        blank=True,
        help_text=('Text field to store base64 encoded profile image content.')
    )

    profile_is_public = models.BooleanField(
        default=False,
        help_text=("Enabling this will let other users see your profile "
                   "inlcuding your name, about, website, where you are on the "
                   "course")
    )

    email_is_public = models.BooleanField(
        default=False,
        help_text=("Enabling this will let other users see your email address; "
                   "profile needs to be set to public as well")
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        """  Return Class object to string via the user email value  """
        return self.slack_display_name

    def human_readable_current_lms_module(self):
        return self.current_lms_module.replace('_', ' ')

    def to_team_member(self):
        return {
            'userid': self.id,
            'name': self.slack_display_name or self.email,
            'level': LMS_LEVELS[self.current_lms_module]
        }
