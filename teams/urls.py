from django.urls import path

from .views import view_team, create_teams, clear_teams, create_project,\
                   rename_team, create_group_im, view_team_calendar, \
                   view_team_competencies
from showcase.views import create_or_update_showcase

urlpatterns = [
    path("<int:team_id>/", view_team,
         name="view_team"),
    path("<int:team_id>/project/", create_project, name="create_project"),
    path("<int:team_id>/showcase/",
         create_or_update_showcase, name="create_or_update_showcase"),
    path("<int:team_id>/create_group_im/", create_group_im,
         name="create_group_im"),
    path("<int:team_id>/rename/", rename_team, name="rename_team"),
    path("<int:team_id>/calendar/", view_team_calendar,
         name="view_team_calendar"),
    path("<int:team_id>/competencies/", view_team_competencies,
         name="view_team_competencies"),
    path("create/", create_teams, name="create_teams"),
    path("clear/", clear_teams, name="clear_teams"),
]
