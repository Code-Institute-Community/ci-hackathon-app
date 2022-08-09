from django.urls import path

from . import views
from showcase.views import create_or_update_showcase

urlpatterns = [
    path("<int:team_id>/", views.view_team,
         name="view_team"),
    path("<int:team_id>/project/", views.create_project,
         name="create_project"),
    path("<int:team_id>/showcase/",
         create_or_update_showcase, name="create_or_update_showcase"),
    path("<int:team_id>/create_group_im/", views.create_group_im,
         name="create_group_im"),
    path("<int:team_id>/rename/", views.rename_team, name="rename_team"),
    path("<int:team_id>/calendar/", views.view_team_calendar,
         name="view_team_calendar"),
    path("<int:team_id>/competencies/", views.view_team_competencies,
         name="view_team_competencies"),
    path("create/", views.create_teams, name="create_teams"),
    path("clear/", views.clear_teams, name="clear_teams"),
]
