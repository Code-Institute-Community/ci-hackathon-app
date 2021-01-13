from django import forms

from accounts.models import Organisation
from .models import Hackathon
from .lists import STATUS_TYPES_CHOICES, JUDGING_STATUS_CHOICES

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
                'rows': 3,
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
    judging_status = forms.CharField(
        label="Judging Status",
        required=True,
        widget=forms.Select(choices=JUDGING_STATUS_CHOICES),
    )
    organisation = forms.ModelChoiceField(
        label="Organisation",
        queryset=Organisation.objects.order_by('display_name'),
    )

    class Meta:
        model = Hackathon
        fields = ['display_name', 'description', 'theme', 'start_date',
                  'end_date', 'status', 'judging_status', 'organisation',
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