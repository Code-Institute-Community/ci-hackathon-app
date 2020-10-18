from django.forms import ModelForm
from .models import Hackathon


class HackathonForm(ModelForm):
    class Meta:
        model = Hackathon
        fields = ['display_name', 'description', 'theme', 'start_date', 'end_date', 'judges', 'organiser']
