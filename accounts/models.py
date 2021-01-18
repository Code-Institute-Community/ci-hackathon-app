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
        max_length=50,
        blank=False,
        default='',
        choices=LMS_MODULES_CHOICES
    )

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name='user_organisation',
        default=Organisation.DEFAULT_PK
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        """  Return Class object to string via the user email value  """
        return self.username

    def human_readable_current_lms_module(self):
        return self.current_lms_module.replace('_', ' ')

    def to_team_member(self):
        return {
            'userid': self.id,
            'name': self.username,
            'level': LMS_LEVELS[self.current_lms_module]
        }
