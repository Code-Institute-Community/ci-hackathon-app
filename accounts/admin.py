from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    fields = (
        'slack_display_name',
        'user_type',
        'current_lms_module',
    )


admin.site.register(Profile, ProfileAdmin)
