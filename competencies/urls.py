from django.urls import path

from competencies.views import self_assess_competencies, list_competencies, \
                               create_competency, edit_competency, \
                               create_competency_difficulty, \
                               edit_competency_difficulty

urlpatterns = [
    path('', self_assess_competencies, name="self_assess_competencies"),
    path('list', list_competencies, name="list_competencies"),
    path('create', create_competency, name="create_competency"),
    path('edit/<int:competency_id>', edit_competency, name="edit_competency"),
    path('difficulty/create', create_competency_difficulty,
         name="create_competency_difficulty"),
    path('difficulty/edit/<int:competency_difficulty_id>', edit_competency_difficulty,
         name="edit_competency_difficulty"),
]
