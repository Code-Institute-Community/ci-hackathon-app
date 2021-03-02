from django.urls import path
from .views import (
    HackathonListView,
    create_hackathon,
    update_hackathon,
    delete_hackathon,
    HackathonDetailView,
    enroll_toggle,
    judging,
    check_projects_scores,
    view_hackathon,
    update_hackathon_status,
    change_awards,
    hackathon_stats,
    list_teams_for_scoring
)
from teams.views import change_teams

urlpatterns = [
    path('', HackathonListView.as_view(), name="hackathon-list"),
    path("<int:hackathon_id>/team/<int:team_id>/judging/",
         judging, name="judging"),
    path("<int:hackathon_id>/final_score/", check_projects_scores,
         name="final_score"),
    path("<int:hackathon_id>/change_teams/", change_teams, name="change_teams"),
    path("<int:hackathon_id>/awards/", change_awards, name="awards"),
    path("create_hackathon", create_hackathon, name='create_hackathon'),
    path("<int:hackathon_id>/", view_hackathon,
         name='view_hackathon'),
    path("<int:hackathon_id>/update", update_hackathon,
         name="update_hackathon"),
     path("<int:hackathon_id>/update_hackathon_status", update_hackathon_status,
         name="update_hackathon_status"),
    path("<int:hackathon_id>/delete", delete_hackathon,
         name="delete_hackathon"),
    path('enroll/', enroll_toggle, name='enroll_toggle'),
    path('stats/', hackathon_stats, name='hackathon_stats'),
    path('<int:hackathon_id>/score_teams/', list_teams_for_scoring,
        name="list_teams_for_scoring"),
]
