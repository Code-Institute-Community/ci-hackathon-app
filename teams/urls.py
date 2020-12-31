from django.urls import path

from .views import view_team, create_teams, clear_teams

urlpatterns = [
     path("<int:team_id>/", view_team,
          name="view_team"),
     path("create/", create_teams, name="create_teams"),
     path("clear/", clear_teams, name="clear_teams"),
]
