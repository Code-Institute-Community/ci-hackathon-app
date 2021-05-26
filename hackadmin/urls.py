from django.urls import path
from .views import (
    hackadmin_panel,
    hackathon_participants,
    all_users,
    remove_participant,
    add_participant,
    add_judge,
)

urlpatterns = [
    path('', hackadmin_panel, name='hackadmin_panel'),
    path('<str:hackathon_id>/participants/', hackathon_participants,
         name='hackathon_participants'),
    path('all_users/', all_users, name='all_users'),
    path('<str:hackathon_id>/remove_participant/', remove_participant,
         name='remove_participant'),
    path('<str:hackathon_id>/add_participant/', add_participant,
         name='add_participant'),
    path('add_judge/', add_judge,
         name='add_judge'),
]
