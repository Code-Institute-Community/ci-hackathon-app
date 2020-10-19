from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.db.models.signals import post_delete

"""List of user types to be passed into dropdown of same name for each 
user selection."""
user_types = [
    ('', 'Select Post Category'),
    ('participant', 'Participant'),
    ('staff', 'Staff'),
    ('admin', 'Admin'),
]

"""List of CI LMS modules to be passed into dropdown of same name for each 
user selection."""
lms_modules = [
    ('', 'Select Learning Stage'),
    ('programme preliminaries', 'Programme Preliminaries'),
    ('programming paradigms', 'Programming Paradigms'),
    ('html fundamentals', 'HTML Fundamentals'),
    ('css fundamentals', 'CSS Fundamentals'),
    ('user centric frontend development', 'User Centric Frontend Development'),
    ('javascript fundamentals', 'Javascript Fundamentals'),
    ('interactive frontend development', 'Interactive Frontend Development'),
    ('python fundamentals', 'Python Fundamentals'),
    ('practical python', 'Practical Python'),
    ('data centric development', 'Data Centric Development'),
    ('full stack frameworks with django', 'Full Stack Frameworks with Django'),
    ('alumni', 'Alumni'),
    ('staff', 'Staff'),
]


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, default=1,
        related_name='profile',
        on_delete=models.CASCADE
    )
    slack_display_name = models.CharField(
        max_length=80,
        blank=False,
        null=True
    )
    user_type = models.CharField(
        max_length=20,
        blank=False,
        null=True,
        choices=user_types
    )
    current_lms_module = models.CharField(
        max_length=35,
        blank=False,
        null=True,
        choices=lms_modules
    )

    def save(self, *args, **kwargs):
        # when signup takes place
        try:
            self.slack_display_name = self.user.slack_display_name
            self.user_type = self.user.user_type
            self.current_lms_module = self.user.current_lms_module
        # when saving via admin panel
        except:
            self.slack_display_name = self.user.profile.slack_display_name
            self.user_type = self.user.profile.user_type
            self.current_lms_module = self.user.profile.current_lms_module

        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


@receiver(user_signed_up)
def user_signed_up(request, user, **kwargs):
    # capture server request object in dict from QueryDict, for easy accessing
    # of headers within
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

    # Save linked instance of user object to profile model
    Profile.objects.create(user=user)


@receiver(post_delete, sender=Profile)
def post_delete_user(sender, instance, *args, **kwargs):
    """
    admin - delete user at same time as profile deletion
    """
    if instance:
        instance.user.delete()
