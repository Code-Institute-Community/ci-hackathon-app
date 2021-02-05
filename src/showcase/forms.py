from django import forms

from .models import Showcase
from hackathon.models import HackTeam, HackProject


class ShowcaseForm(forms.ModelForm):
    """ Form to create or update Showcase """
    class Meta:
        model = Showcase
        fields = ['hack_project', 'showcase_participants', 'is_public',
                  'display_name']

    def __init__(self,*args,**kwargs):
        team_id = kwargs.pop('team_id', None)
        team = HackTeam.objects.filter(id=team_id).first()
        # call standard __init__
        super(ShowcaseForm, self).__init__(*args, **kwargs)
        self.fields['showcase_participants'] = forms.ModelMultipleChoiceField(
            queryset=team.participants.all(),
            widget=forms.SelectMultiple(attrs={
                    'size': '7'
                })
            )
            
        self.fields['hack_project'].widget = forms.HiddenInput()
