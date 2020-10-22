from django.db import models
from django.contrib.auth.models import AbstractUser

from .lists import USER_TYPES_CHOICES, LMS_MODULES_CHOICES


class CustomUser(AbstractUser):
    """ Custom user model extending the basic AbstractUser model """
    slack_display_name = models.CharField(
        max_length=80,
        blank=False,
        null=True
    )

    user_type = models.CharField(
        max_length=20,
        blank=False,
        null=True,
        choices=USER_TYPES_CHOICES
    )

    current_lms_module = models.CharField(
        max_length=35,
        blank=False,
        null=True,
        choices=LMS_MODULES_CHOICES
    )

    def __str__(self):
        """  Return Class object to string via the user email value  """
        return self.username
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
