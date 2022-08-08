from django.test import TestCase

from accounts.models import CustomUser as User, Organisation
from competencies.helpers import get_or_create_competency_assessment, \
                                 populate_competency_assessment_for_formset
from competencies.models import Competency, CompetencyAssessment, \
                                CompetencyDifficulty, \
                                CompetencyAssessmentRating


class CompetencyAssessmentTest(TestCase):
    def setUp(self):
        self.organisation = Organisation.objects.create()
        self.user = User.objects.create(
            username="testuser",
            slack_display_name="testuser",
        )
        self.user2 = User.objects.create(
            username="testuser2",
            slack_display_name="testuser2",
        )
        
        self.assessment = CompetencyAssessment.objects.create(
            user=self.user2,
            is_visible=False,
        )

        competency_difficulty = CompetencyDifficulty.objects.create(
            created_by=self.user,
            display_name='Easy',
        )
        self.competency = Competency.objects.create(
            created_by=self.user,
            display_name='HTML',
            perceived_difficulty=competency_difficulty,
        )
        self.competency2 = Competency.objects.create(
            created_by=self.user,
            display_name='CSS',
            perceived_difficulty=competency_difficulty,
        )
        CompetencyAssessmentRating.objects.create(
            user_assessment=self.assessment,
            competency=self.competency,
            rating='know_it'
        )

    def test_get_or_create_competency_assessment(self):
        data = {
            'user': self.user.id,
            'is_visible': True
        }
        competency_assessment = get_or_create_competency_assessment(data)
        self.assertTrue(isinstance(competency_assessment,
                                   CompetencyAssessment))

    def test_get_or_create_competency_assessment_error(self):
        data = {}
        competency_assessment = get_or_create_competency_assessment(data)
        self.assertIsNone(competency_assessment)

    def test_get_or_create_competency_assessment_existing_assssment(self):
        data = {'user': self.user2.id}
        competency_assessment = get_or_create_competency_assessment(data)
        self.assertEquals(self.assessment.id, competency_assessment.id)
    
    def test_populate_competency_assessment_for_formset(self):
        data = {
            'form-0-competency': 1,
            'form-1-competency': 2,
        }
        populate_competency_assessment_for_formset(self.assessment, data)
        self.assertEquals(data['form-0-user_assessment'], 1)
        self.assertEquals(data['form-1-user_assessment'], 1)

        data['form-2-competency'] = 3
        populate_competency_assessment_for_formset(self.assessment, data)
        self.assertEquals(data['form-0-user_assessment'], 1)
        self.assertEquals(data['form-1-user_assessment'], 1)
        self.assertEquals(data['form-2-user_assessment'], 1)

    def test_get_user_rating(self):
        assessment = self.competency.get_user_rating(self.user2)
        self.assertEquals(assessment.rating, 'know_it')
        
        assessment = self.competency2.get_user_rating(self.user2)
        self.assertIsNone(assessment)