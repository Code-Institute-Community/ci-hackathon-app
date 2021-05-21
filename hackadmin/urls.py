from django.urls import path
from .views import (
    hackadmin_panel,
    hackathon_participants,
    all_users,
)

urlpatterns = [
    path('', hackadmin_panel, name='hackadmin_panel'),
    path('<str:hackathon_id>/participants/', hackathon_participants,
        name='hackathon_participants'),
    path('all_users/', all_users, name='all_users'),
]
