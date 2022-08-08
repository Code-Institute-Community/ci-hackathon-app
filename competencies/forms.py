from django import forms
from django.forms import BaseModelFormSet

from competencies.models import Competency, CompetencyDifficulty, \
                                CompetencyAssessment, CompetencyAssessmentRating


class RequiredModelFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredModelFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False
            form.use_required_attribute = True


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


class CompetencyAssessmentForm(forms.ModelForm):
    is_visible = forms.BooleanField(
        required=False,
        label="Make my assessment visible to my teams and facilitators")
    class Meta:
        model = CompetencyAssessment
        fields = ['user', 'is_visible']

class CompetencyAssessmentRatingForm(forms.ModelForm):
    competency = forms.ModelChoiceField(
        queryset=Competency.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control disabled-select',
        }))
    class Meta:
        model = CompetencyAssessmentRating
        fields = ['id', 'user_assessment', 'competency', 'rating']
