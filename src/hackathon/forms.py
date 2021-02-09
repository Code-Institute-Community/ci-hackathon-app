from django import forms
from django.forms import BaseModelFormSet

from accounts.models import Organisation
from .models import Hackathon, HackProject, HackAward,\
                    HackProjectScoreCategory, HackAwardCategory
from .lists import STATUS_TYPES_CHOICES

class HackathonForm(forms.ModelForm):
    """ A form to enable users to add hackathon events via the frontend site.
     The form renders the fields that require value inputs from the user, along with some basic validation. """
    display_name = forms.CharField(
        label='Display Name',
        min_length=5,
        max_length=254,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Event name...'
            }
        ),
        required=True
    )
    description = forms.CharField(
        label="Description",
        min_length=10,
        max_length=3000,
        widget=forms.Textarea(
            attrs={
                'rows': 4,
                'placeholder': 'Tell us more about this event...'
            }
        )
    )
    theme = forms.CharField(
        label='Theme',
        min_length=5,
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
    teamsize = forms.IntegerField(
        label="Team Size",
        required=True,
    )
    organisation = forms.ModelChoiceField(
        label="Organisation",
        queryset=Organisation.objects.order_by('display_name'),
    )
    score_categories = forms.ModelMultipleChoiceField(
        queryset=HackProjectScoreCategory.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'size': '5'
        })
    )

    class Meta:
        model = Hackathon
        fields = ['display_name', 'description', 'theme', 'start_date',
                  'end_date', 'status', 'organisation', 'score_categories',
                  'teamsize',
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
                    hackteam__in=hackathon.teams.all()).order_by('display_name')
            hack_award_categories = HackAwardCategory.objects.filter(
                    award__in=hackathon.awards.all()).order_by(
                        'display_name')
            self.fields['hack_award_category'] = forms.ModelChoiceField(
                # queryset=hackathon.hackaward.hack_award_categories.all())
                queryset=hack_award_categories)
            self.fields['winning_project'] = forms.ModelChoiceField(
                queryset=hack_projects)
            self.fields['winning_project'].required = False
