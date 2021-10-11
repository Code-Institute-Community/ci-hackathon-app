from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import CustomUser, Organisation, EmailTemplate, Status
from accounts.models import SlackSiteSettings


class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': (
            'username', 'first_name', 'last_name',
            'full_name', 'slack_display_name',
            'status', 'organisation',
            'timezone', 'user_type', 'is_external')}),
            'status', 'organisation',
            'user_type', 'is_external')}),
        ('Permissions', {'fields': (
            'is_active', 'is_staff', 'is_superuser',
            'profile_is_public', 'email_is_public',
            'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    limited_fieldsets = (
        (None, {'fields': ('email',)}),
        ('Personal info', {'fields': ('full_name',
                                      'slack_display_name',
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
    list_display = ('email', 'username', 'full_name', 'is_superuser', 'user_type',
                    'is_external', 'status')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups',
                   'is_external')
    search_fields = ('full_name', 'email', 'slack_display_name')
    ordering = ('email',)

    readonly_fields = ('last_login', 'date_joined', 'user_type')


class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'subject', 'template_name', 'is_active', )


# sign-in via allauth required before accessing the admin panel
admin.site.login = login_required(admin.site.login)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Organisation)
admin.site.register(SlackSiteSettings)
admin.site.register(EmailTemplate, EmailTemplateAdmin)
admin.site.register(Status)

