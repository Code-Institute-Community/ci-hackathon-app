from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    # Defining fields for Admin panel
    fields = (
        'slack_display_name',
        'user_type',
        'current_lms_module',
    )


admin.site.register(Profile, ProfileAdmin)

