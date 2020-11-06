from django.urls import path

from .views import distribute_teams

urlpatterns = [
    path("<int:hackathon_id>/distribute", distribute_teams,
         name="distribute_teams"),
]
