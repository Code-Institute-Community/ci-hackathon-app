from django.core.exceptions import ObjectDoesNotExist

from competencies.forms import CompetencyAssessmentForm
from competencies.models import CompetencyAssessment


def get_or_create_competency_assessment(data):
    try:
        existing_assessment = CompetencyAssessment.objects.get(
            user=data.get('user'))
        existing_assessment.is_visible = data.get('is_visible') == 'on'
        existing_assessment.save()
        return existing_assessment
    except ObjectDoesNotExist:
        # If no assessment exists, just continue
        pass

    form = CompetencyAssessmentForm(data)
    if form.is_valid():
        return form.save()
    return


def populate_competency_assessment_for_formset(competency_assessment, data):
    keys = [key for key in data.keys()
            if key.endswith('-competency')]

    for key in keys:
        assessment_key = key.replace('-competency', '-user_assessment')
        data[assessment_key] = competency_assessment.id
