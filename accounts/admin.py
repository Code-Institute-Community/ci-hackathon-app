from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm, \
    UserChangeForm, UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import CustomUser, Organisation


class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': (
            'full_name', 'slack_display_name', 'user_type',
            'current_lms_module', 'organisation')}),
        ('Permissions', {'fields': (
            'is_active', 'is_staff', 'is_superuser', 
            'profile_is_public', 'email_is_public',
            'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    limited_fieldsets = (
        (None, {'fields': ('email',)}),
        ('Personal info', {'fields': ('full_name',
                                      'slack_display_name', 'user_type',
                                      'organisation')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )

    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'full_name', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('full_name', 'email')
    ordering = ('email',)
    readonly_fields = ('last_login', 'date_joined',)


# sign-in via allauth required before accessing the admin panel
admin.site.login = login_required(admin.site.login)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Organisation)
