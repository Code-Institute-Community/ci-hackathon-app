from django.urls import path
from . import views
from .views import HackathonListView, create_hackathon, delete_hackathon

urlpatterns = [
    path('', HackathonListView.as_view(), name="hackathon-list"),
    path("<int:hack_id>/team/<int:team_id>/judging/", views.judging, name="judging"),
    path("create_hackathon", create_hackathon, name='create_hackathon'),
    path("<int:hackathon_id>/delete_hackathon", delete_hackathon, name="delete_hackathon"),
]

