from django import forms

from hackathon.models import HackProject


class HackProjectForm(forms.ModelForm):
    """ A form to create a new team project """
    display_name = forms.CharField(
        label='Display name',
        required=True
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows':4}),
        label='Description',
        required=True
    )
    technologies_used = forms.CharField(
        label='Technologies used',
        required=True
    )
    github_url = forms.CharField(
        label='GitHub url',
        required=False
    )
    deployed_url = forms.CharField(
        label='Deployed url',
        required=False
    )
    speaker_name = forms.CharField(
        label='Speaker name',
        required=False
    )
    share_permission = forms.CharField(
        label='Grant permission to publicly share the project',
        widget=forms.CheckboxInput(),
        required=False
    ) 

    class Meta:
        model = HackProject
        fields = ['display_name', 'description', 'technologies_used',
                  'github_url', 'deployed_url', 'speaker_name',
                  'share_permission',
                  ]
