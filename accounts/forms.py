from django import forms
from allauth.account.forms import SignupForm

from .lists import USER_TYPES_CHOICES, LMS_MODULES_CHOICES


class ExtendedSignupForm(SignupForm):
    """
    Extending default Django allauth Signup Form to include fields to capture:
    - first name/last name/slack display name/user type/current lms module
    """
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    slack_display_name = forms.CharField(max_length=25)
    user_type = forms.ChoiceField(
        choices=USER_TYPES_CHOICES
    )
    current_lms_module = forms.ChoiceField(
        choices=LMS_MODULES_CHOICES
    )

    def __init__(self, *args, **kwargs):
        """
        Setting unique attribute of the class instance and calling the parent
        class.
        Resetting the form autofocus to 'email' as the first displayed field.
        """
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['autofocus'] = True

    def custom_signup(self, request, user):
        """
        Custom logic to ensure clean data via the form response.
        """
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.slack_display_name = self.cleaned_data["slack_display_name"]
        user.user_type = self.cleaned_data["user_type"]
        user.current_lms_module = self.cleaned_data["current_lms_module"]

