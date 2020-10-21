from django import forms
from .models import Hackathon


class HackathonForm(forms.ModelForm):
    display_name = forms.CharField(
        label='Display Name',
        min_length=5,
        max_length=254,
        widget=forms.TextInput(),
        required=True
    )
    description = forms.CharField(
        label="Description",
        min_length=10,
        max_length=3000,
        widget=forms.Textarea(
            attrs={
                'rows': 3
            }
        ),
        required=True
    )
    theme = forms.CharField(
        label='Theme',
        min_length=5,
        max_length=254,
        widget=forms.TextInput(),
        required=True
    )
    start_date = forms.DateTimeField(
        label="Start Date",
        input_formats=['%d/%m/%Y %H:%M'],
        required=True
    )
    end_date = forms.DateTimeField(
        label="End Date",
        input_formats=['%d/%m/%Y %H:%M'],
        required=True
    )

    class Meta:
        model = Hackathon
        fields = ['display_name', 'description', 'theme', 'start_date', 'end_date']
