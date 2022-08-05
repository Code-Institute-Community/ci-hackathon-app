from django.db import models

from accounts.models import CustomUser as User

ASSESSMENT_RATING_CHOICES = [
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

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name = 'Competency'
        verbose_name_plural = 'Competencies'


class CompetencySelfAssessment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="competencies")
    assessment_rating = models.CharField(
        default="", max_length=50, choices=ASSESSMENT_RATING_CHOICES,
        null=True, blank=True)

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name = 'Competency Self Assessment'
        verbose_name_plural = 'Competency Self Assessments'
