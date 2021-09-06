from django import forms
from django.contrib.auth import get_user_model

from .lists import LMS_MODULES_CHOICES, TIMEZONE_CHOICES
from .models import CustomUser, Status


class SignupForm(forms.Form):
    """
        Custom Signup form overriding the standard all_auth Signup form
        Additional fields include: first_name | last_name |
        slack_display_name | user_type | current lms module | organisation
    """
    full_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Full Name'}),
        label='')
    slack_display_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Slack Display Name'}),
        label='')
    status = forms.ModelChoiceField(
        queryset=Status.objects.filter(admin_only=False),
        label="Where are you currently in the programme?"
    )
    timezone = forms.CharField(
        widget=forms.Select(choices=TIMEZONE_CHOICES),
        label="Timezone"
    )

    class Meta:
        fields = (
            'email', 'password1', 'password2', 'slack_display_name',
            'status', 'timezone',
        )
        model = get_user_model()

    def signup(self, request, user):
        """ Method overriding the all_auth signup functionality """
        user.full_name = self.cleaned_data['full_name']
        user.username = self.cleaned_data['email']
        user.slack_display_name = self.cleaned_data['slack_display_name']
        user.current_lms_module = self.cleaned_data['status']
        user.timezone = self.cleaned_data['timezone']
        user.save()


class EditProfileForm(forms.ModelForm):
    """
        Using ModelForm to directly convert the CustomUser model into the
        EditProfileForm form.
    """
    full_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Full Name'}),
        label='')
    slack_display_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Slack Display Name'}),
        label='')
    # TODO: Change this based on privileges
    status = forms.ModelChoiceField(
        queryset=Status.objects.filter(admin_only=False),
        label="Where are you currently in the programme?"
    )
    about = forms.CharField(widget=forms.Textarea(), required=False)
    website_url = forms.CharField(required=False)
    timezone = forms.CharField(
        widget=forms.Select(choices=TIMEZONE_CHOICES),
        required=True,
    )

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'full_name',
            'about',
            'slack_display_name',
            'status',
            'website_url',
            'timezone',
            'profile_is_public',
            'email_is_public',
        )

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)

        super(EditProfileForm, self).__init__(*args, **kwargs)

        if instance:
            is_admin = instance.is_superuser or instance.is_staff
            if is_admin:
                self.fields['status'].queryset = Status.objects.filter(
                    organisation=instance.organisation)
