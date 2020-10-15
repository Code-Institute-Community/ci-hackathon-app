  
from django import forms
from .models import Submission

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('team_name', 'speaker_name','repo_url','deployed_url')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'team_name': 'Team Name',
            'speaker_name': 'Speaker Name',
            'repo_url': 'Github Repository URL',
            'deployed_url': 'Deployed URL',
        }

        self.fields['team_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False