from django.urls import path

from .views import distribute_teams, view_team, create_teams

urlpatterns = [
     path("distribute/<int:hackathon_id>/", distribute_teams,
          name="distribute_teams"),
     path("<int:team_id>/", view_team,
          name="view_team"),
     path("create/", create_teams, name="create_teams"),
]
