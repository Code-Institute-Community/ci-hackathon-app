from django.urls import path

from competencies.views import self_assess_competencies, list_competencies, \
                               create_competencies, edit_competencies, \
                               create_competency_difficulty, \
                               edit_competency_difficulty

urlpatterns = [
    path('', self_assess_competencies, name="self_assess_competencies"),
    path('list', list_competencies, name="list_competencies"),
    path('create', create_competencies, name="create_competencies"),
    path('edit', edit_competencies, name="edit_competencies"),
    path('difficulty/create', create_competency_difficulty,
         name="create_competency_difficulty"),
    path('difficulty/edit', edit_competency_difficulty,
         name="edit_competency_difficulty"),
]
