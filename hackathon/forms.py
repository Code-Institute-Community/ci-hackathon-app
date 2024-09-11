from django import forms

from accounts.models import Organisation
from .models import Hackathon, HackProject, HackAward, HackTeam, \
                    HackProjectScoreCategory, HackAwardCategory
from .lists import STATUS_TYPES_CHOICES


class HackathonForm(forms.ModelForm):
    """ A form to enable users to add hackathon events via the frontend site.
    The form renders the fields that require value inputs from the user,
    along with some basic validation. """
    display_name = forms.CharField(
        label='Display Name',
        max_length=254,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Event name...'
            }
        ),
        required=True
    )
    tag_line = forms.CharField(
        label="Tag Line",
        max_length=254,
    )
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(
            attrs={
                'rows': 4,
                'placeholder': 'Tell us more about this event...'
            }
        )
    )
    theme = forms.CharField(
        label='Theme',
        max_length=254,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Event theme...'
            }
        ),
        required=True
    )
    start_date = forms.DateTimeField(
        label="Start Date",
        input_formats=['%d/%m/%Y %H:%M'],
        required=True,
        widget=forms.DateTimeInput(
            format='%d/%m/%Y %H:%M',
            attrs={
                'placeholder': 'DD/MM/YYYY HH:MM',
                'autocomplete': 'off'
            }
        ),
    )
    end_date = forms.DateTimeField(
        label="End Date",
        input_formats=['%d/%m/%Y %H:%M'],
        required=True,
        widget=forms.DateTimeInput(
            format='%d/%m/%Y %H:%M',
            attrs={
                'placeholder': 'DD/MM/YYYY HH:MM',
                'autocomplete': 'off'
            }
        ),
    )
    status = forms.CharField(
        label="Status",
        required=True,
        widget=forms.Select(choices=STATUS_TYPES_CHOICES),
    )
    team_size = forms.IntegerField(
        label="Team Size",
        required=True,
        widget=forms.TextInput(attrs={'min': 3, 'max': 6, 'type': 'number'})
    )
    organisation = forms.ModelChoiceField(
        label="Organisation",
        queryset=Organisation.objects.order_by('display_name'),
    )
    score_categories = forms.ModelMultipleChoiceField(
        queryset=HackProjectScoreCategory.objects.filter(is_active=True),
        widget=forms.SelectMultiple(attrs={
            'size': '5'
        })
    )
    is_public = forms.BooleanField(required=False)
    is_register = forms.BooleanField(required=False, label="Allow external registrations")
    google_registration_form = forms.URLField(
        label="External Registration Form",
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Add form url if the event is open to external participants'
            }
        )
    )
    max_participants = forms.IntegerField(
        label="Max Participants",
        required=False,
        widget=forms.TextInput({'type': 'number', 'placeholder': 'Leave empty for no max'})
    )

    class Meta:
        model = Hackathon
        fields = ['display_name', 'description', 'theme', 'start_date',
                  'end_date', 'status', 'organisation', 'score_categories',
                  'team_size', 'tag_line', 'is_public', 'max_participants',
                  'is_register', 'google_registration_form'
                  ]

    def __init__(self, *args, **kwargs):
        super(HackathonForm, self).__init__(*args, **kwargs)
        self.fields['organisation'].empty_label = None


class ChangeHackathonStatusForm(forms.ModelForm):
    status = forms.CharField(
        label="Status",
        required=True,
        widget=forms.Select(choices=STATUS_TYPES_CHOICES),
    )

    class Meta:
        model = Hackathon
        fields = ['start_date', 'end_date', 'status']
        widgets = {
            'start_date': forms.HiddenInput(),
            'end_date': forms.HiddenInput()
            }


class HackTeamForm(forms.ModelForm):
    display_name = forms.CharField(
        label="Team Name",
        required=True,
        disabled=True,
    )

    class Meta:
        model = HackTeam
        fields = ['id', 'display_name', 'mentor']

    def __init__(self, *args, **kwargs):
        hackathon_id = kwargs.pop('hackathon_id', None)
        hackathon = Hackathon.objects.filter(id=hackathon_id).first()
        super(HackTeamForm, self).__init__(*args, **kwargs)

        if hackathon:
            judges = hackathon.judges.all().order_by('slack_display_name')
            self.fields['mentor'] = forms.ModelChoiceField(
                queryset=judges)
            self.fields['mentor'].required = False
            self.fields['mentor'].label = 'Facilitator'


class HackAwardForm(forms.ModelForm):
    """ Form to create or edit HackAwards """
    hack_award_category = forms.ModelChoiceField(
        label="Award Type",
        queryset=HackAwardCategory.objects.order_by('display_name'),
        required=True,
    )

    winning_project = forms.ModelChoiceField(
        label="Winning Project",
        queryset=HackProject.objects.order_by('display_name'),
        required=False
    )

    class Meta:
        model = HackAward
        fields = ('id', 'hack_award_category', 'winning_project')

    def __init__(self, *args, **kwargs):
        hackathon_id = kwargs.pop('hackathon_id', None)
        hackathon = Hackathon.objects.filter(id=hackathon_id).first()
        super(HackAwardForm, self).__init__(*args, **kwargs)
        # Prepopulate dropdowns so only hackathon specific award categories and
        # winning_projects can be chosen if a hackathon_id is specified
        if hackathon:
            hack_projects = HackProject.objects.filter(
                    hackteam__in=hackathon.teams.all()).order_by(
                        'display_name')
            hack_award_categories = HackAwardCategory.objects.filter(
                    award__in=hackathon.awards.all()).order_by(
                        'display_name')
            self.fields['hack_award_category'] = forms.ModelChoiceField(
                queryset=hack_award_categories)
            self.fields['winning_project'] = forms.ModelChoiceField(
                queryset=hack_projects)
            self.fields['winning_project'].required = False
