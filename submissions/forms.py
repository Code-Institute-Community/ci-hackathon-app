from django import forms
from hackathon.models import HackProject


class HackProjectSubmissionForm(forms.ModelForm):
    class Meta:
        model = HackProject
        exclude = ('mentor',)
        fields = ('display_name', 'description', 'github_url',
                  'deployed_url', 'speaker_name','share_permission')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'display_name': 'Project Name',
            'speaker_name': 'Speaker(s) Name',
            'description': 'Description',
            'github_url': 'GitHub Repository URL',
            'deployed_url': 'Deployed URL',
            'share_permission': 'Share Permission',
        }

        self.fields['display_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False
