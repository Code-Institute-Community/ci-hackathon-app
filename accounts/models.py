from datetime import datetime
from enum import Enum
import pytz

from django.db import models
from django.contrib.auth.models import AbstractUser

from .lists import LMS_MODULES_CHOICES, TIMEZONE_CHOICES
from main.models import SingletonModel
from teams.lists import LMS_LEVELS

COMMUNICATION_CHANNEL_TYPES = [
    ('slack_private_channel', 'Private Slack Channel'),
    ('other', 'Other'),
]


class UserType(Enum):
    SUPERUSER = 0
    STAFF = 1
    FACILITATOR_ADMIN = 2
    FACILITATOR_JUDGE = 3
    FACILITATOR = 4
    PARTICIPANT = 5
    EXTERNAL_USER = 6
    PARTNER_ADMIN = 7
    PARTNER_JUDGE = 8
    PARTNER_USER = 9


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
        help_text=("Enabling this will let other users see your email "
                   "address; profile needs to be set to public as well")
    )

    is_external = models.BooleanField(
        default=False,
        help_text=("Set to True if a user signs up through an external "
                   "registration link")
    )

    timezone = models.CharField(
        max_length=255,
        blank=False,
        default='Europe/London',
        choices=TIMEZONE_CHOICES,
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
        teams = self.participated_hackteams.filter(
            hackathon__status='finished')
        return {
            'userid': self.id,
            'name': self.slack_display_name or self.email,
            'level': LMS_LEVELS.get(self.current_lms_module) or 1,
            'timezone': self.timezone_to_offset(),
            'num_hackathons': teams.count(),
            'participant_label': self.participant_label(),
        }

    def timezone_to_offset(self):
        if not self.timezone:
            return
        offset = datetime.now(pytz.timezone(self.timezone)).strftime('%z')
        return f'UTC{offset[:-2]}'

    def participant_label(self):
        teams = self.participated_hackteams.filter(
            hackathon__status='finished')
        if teams.count() == 0:
            return 'Hackathon Newbie'
        elif teams.count() < 2:
            return 'Hackathon Enthusiast'
        else:
            return 'Hackathon Veteran'
    
    def is_participant(self, hackathon):
        if not hackathon:
            return False
        
        return self in hackathon.participants.all()


    @property
    def user_type(self):
        """ Return the user's main designation.
        This is something that we would need to continuously evolve.
        """
        groups = self.groups.all()
        if self.is_staff and self.is_superuser:
            return UserType.SUPERUSER
        elif self.is_staff:
            return UserType.STAFF
        elif self.organisation.id != 1:
            # This is assuming that the first organisation entered is the
            # "host organisation"
            # TODO: Add a model or environment variable to determine which is
            # the host organisation
            if groups.filter(name='FACILITATOR_ADMIN'):
                return UserType.PARTNER_ADMIN
            elif groups.filter(name='FACILITATOR_JUDGE'):
                return UserType.PARTNER_JUDGE
            else:
                return UserType.PARTNER_USER
        elif not groups:
            if self.is_external:
                return UserType.EXTERNAL_USER
            return UserType.PARTICIPANT
        else:
            if groups.filter(name='FACILITATOR_ADMIN'):
                return UserType.FACILITATOR_ADMIN
            elif groups.filter(name='FACILITATOR_JUDGE'):
                return UserType.FACILITATOR_JUDGE
            elif groups.filter(name='FACILITATOR'):
                return UserType.FACILITATOR
            else:
                # A non-specified group
                return None


class SlackSiteSettings(SingletonModel):
    """ Model to set how the showcase should be constructed"""
    slack_admins = models.ManyToManyField(CustomUser,
                                          related_name="slacksitesettings")
    enable_welcome_emails = models.BooleanField(default=True)
    communication_channel_type = models.CharField(
        max_length=50, choices=COMMUNICATION_CHANNEL_TYPES,
        default='slack_private_channel')

    def __str__(self):
        return "Slack Settings"

    class Meta:
        verbose_name = 'Slack Site Settings'
        verbose_name_plural = 'Slack Site Settings'


class EmailTemplate(models.Model):
    display_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    template_name = models.CharField(max_length=255, unique=True)
    subject = models.CharField(max_length=1048)
    plain_text_message = models.TextField()
    html_message = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Email Template'
        verbose_name_plural = 'Email Templates'

    def __str__(self):
        return self.display_name
