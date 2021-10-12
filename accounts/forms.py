from django import forms
from django.contrib.auth import get_user_model

from .models import Status, CustomUser


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
        label="Programming Experience"
    )

    class Meta:
        fields = (
            'email', 'password1',  'password2', 'slack_display_name', 'status',
        )
        model = get_user_model()

    def signup(self, request, user):
        """ Method overriding the all_auth signup functionality """
        user.full_name = self.cleaned_data['full_name']
        user.username = self.cleaned_data['email']
        user.slack_display_name = self.cleaned_data['slack_display_name']
        user.status = self.cleaned_data['status']
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
    status = forms.ModelChoiceField(
        queryset=Status.objects.filter(admin_only=False),
        label="Programming Experience"
    )
    about = forms.CharField(widget=forms.Textarea(), required=False)
    website_url = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'full_name',
            'about',
            'slack_display_name',
            'status',
            'website_url',
            'profile_is_public',
            'email_is_public',
        )

    def __init__(self, *args, **kwargs):
        """ Adding extra dropdown options if user is superuser or staff """
        instance = kwargs.get('instance', None)
        super(EditProfileForm, self).__init__(*args, **kwargs)

        if instance:
            is_admin = instance.is_superuser or instance.is_staff
            if is_admin:
                self.fields['status'].queryset = Status.objects.filter(
                    organisation=instance.organisation)
