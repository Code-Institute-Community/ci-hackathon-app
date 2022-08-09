from django.urls import path

from competencies import views



urlpatterns = [
    path('', views.self_assess_competencies, name="self_assess_competencies"),
    path('list', views.list_competencies, name="list_competencies"),
    path('create', views.create_competency, name="create_competency"),
    path('edit/<int:competency_id>', views.edit_competency,
         name="edit_competency"),
    path('difficulty/create', views.create_competency_difficulty,
         name="create_competency_difficulty"),
    path('difficulty/edit/<int:competency_difficulty_id>', 
         views.edit_competency_difficulty, name="edit_competency_difficulty"),
]
