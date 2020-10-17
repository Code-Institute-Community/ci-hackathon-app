from allauth.account.forms import SignupForm
from django import forms

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


class ExtendedSignupForm(SignupForm):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    slack_display_name = forms.CharField(max_length=25)
    user_type = forms.ChoiceField(
        choices=user_types
    )
    current_lms_module = forms.ChoiceField(
        choices=lms_modules
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def custom_signup(self, request, user):
        user.user_type = self.cleaned_data["user_type"]
        user.current_lms_module = self.cleaned_data["current_lms_module"]
        user.save()
