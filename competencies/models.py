from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from accounts.models import CustomUser as User

ASSESSMENT_RATING_CHOICES = [
    ('no_knowledge', 'I have no knowledge'),
    ('want_to_know', 'Want to know about it'),
    ('learning', 'Learning about it right now'),
    ('know_it', 'I know about this'),
]


class CompetencyDifficulty(models.Model):
    """ A percieved difficulty level of a competency or skill """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   related_name="created_competency_difficulties")
    
    display_name = models.CharField(default="", max_length=255, unique=True)
    numeric_difficulty = models.FloatField(default=1.0)

    def __str__(self):
        return f'{self.display_name} - {self.numeric_difficulty}'

    class Meta:
        verbose_name = 'Competency Difficulty'
        verbose_name_plural = 'Competency Difficulties'


class Competency(models.Model):
    """ A competency or skill that a user can make a self assessment for """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   related_name="created_competencies")

    display_name = models.CharField(default="", max_length=255)
    perceived_difficulty = models.ForeignKey(CompetencyDifficulty,
                                             on_delete=models.CASCADE,
                                             related_name="competencies")
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name = 'Competency'
        verbose_name_plural = 'Competencies'
    
    def get_user_rating(self, user):
        try:
            return self.competency_assessment_ratings.get(
                user_assessment__user=user)
        except ObjectDoesNotExist:
            return



class CompetencyAssessment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    user = models.OneToOneField(User,
                             on_delete=models.CASCADE,
                             related_name="competency_assessment")
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.user.slack_display_name

    class Meta:
        verbose_name = 'Competency Self Assessment'
        verbose_name_plural = 'Competency Self Assessments'


class CompetencyAssessmentRating(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    user_assessment = models.ForeignKey(CompetencyAssessment,
                                        on_delete=models.CASCADE,
                                        related_name="competencies")
    competency = models.ForeignKey(Competency,
                                   on_delete=models.CASCADE,
                                   related_name="competency_assessment_ratings")
    rating = models.CharField(
        default="", max_length=50, choices=ASSESSMENT_RATING_CHOICES,
        null=True, blank=True)

    def __str__(self):
        return f'{self.user_assessment} - {self.rating}'

    class Meta:
        verbose_name = 'Competency Self Assessment Rating'
        verbose_name_plural = 'Competency Self Assessment Ratings'
