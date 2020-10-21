from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    """
    Profile Model Admin Panel setup.
    Returning and displaying the three custom fields from the extended
    allauth signup form.
    """
    fields = (
        'slack_display_name',
        'user_type',
        'current_lms_module',
        'organisation',
    )


admin.site.register(Profile, ProfileAdmin)

