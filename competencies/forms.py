from django import forms

from competencies.models import Competency, CompetencyDifficulty

class CompetencyForm(forms.ModelForm):
    perceived_difficulty = forms.ModelChoiceField(
        queryset=CompetencyDifficulty.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control'
        }))

    class Meta:
        model = Competency
        fields = ['display_name', 'perceived_difficulty']


class CompetencyDifficultyForm(forms.ModelForm):
    class Meta:
        model = CompetencyDifficulty
        fields = ['display_name', 'numeric_difficulty']
