from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model

from .lists import USER_TYPES_CHOICES, LMS_MODULES_CHOICES
from .models import Organisation
from .models import CustomUser


class SignupForm(forms.Form):
    """ 
        Custom Signup form overriding the standard all_auth Signup form 
        Additional fields include: first_name | last_name |
        slack_display_name | user_type | current lms module | organisation
    """
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    slack_display_name = forms.CharField(max_length=30,
                                         label='Slack display name')
    user_type = forms.CharField(widget=forms.Select(
        choices=USER_TYPES_CHOICES))
    current_lms_module = forms.CharField(widget=forms.Select(
        choices=LMS_MODULES_CHOICES))
    organisation = forms.ModelChoiceField(queryset=Organisation.objects.all())

    class Meta:
        fields = (
            'email', 'password1', 'password2',
            'slack_display_name', 'user_type', 'current_lms_module',
            'organisation'
        )
        model = get_user_model()

    def signup(self, request, user):
        """ Method overriding the all_auth signup functionality """
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['email']
        user.slack_display_name = self.cleaned_data['slack_display_name']
        user.user_type = self.cleaned_data['user_type']
        user.current_lms_module = self.cleaned_data['current_lms_module']

        # Setting the correct user permission based on user_type
        # Setting staff and admin to is_active = False by default
        if self.cleaned_data['user_type'] == 'participant':
            user.is_active = True
        elif self.cleaned_data['user_type'] == 'staff':
            user.is_staff = True
            user.is_active = False
        else:
            user.is_staff = True
            user.is_superuser = True
            user.is_active = False

        user.save()


class EditProfileForm(forms.ModelForm):
    """ 
        Using ModelForm to directly convert the CustomUser model into the EditProfileForm form.
    """

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'first_name',
            'last_name',
            'slack_display_name',
            'current_lms_module'
        )
