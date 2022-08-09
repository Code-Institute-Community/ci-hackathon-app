from django.contrib import admin

from competencies.models import (
    Competency, CompetencyDifficulty,
    CompetencyAssessment, CompetencyAssessmentRating)

admin.site.register(CompetencyDifficulty)
admin.site.register(Competency)
admin.site.register(CompetencyAssessment)
admin.site.register(CompetencyAssessmentRating)
