from django.urls import path
from .views import *

urlpatterns = [
    path('', HackathonListView.as_view(), name="hackathon-list"),
    path("<int:hack_id>/team/<int:team_id>/judging/", judging, name="judging"),
    path("create_hackathon", create_hackathon, name='create_hackathon'),
    path("<int:hackathon_id>/view_hackathon", view_hackathon,
         name='view_hackathon'),
    path("<int:hackathon_id>/update_hackathon", update_hackathon,
         name="update_hackathon"),
    path("<int:hackathon_id>/delete_hackathon", delete_hackathon,
         name="delete_hackathon"),
]
