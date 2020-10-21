from django import forms
from .models import Hackathon


class HackathonForm(forms.ModelForm):
    class Meta:
        model = Hackathon
        fields = ['display_name', 'description', 'theme', 'start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        super(HackathonForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget = forms.DateTimeInput(attrs={
            'required': True,
        })
        self.fields['end_date'].widget = forms.DateTimeInput(attrs={
            'required': True,
        })
