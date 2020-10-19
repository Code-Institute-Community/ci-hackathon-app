from django.urls import path
from . import views
from .views import HackathonListView

urlpatterns = [
    path('', HackathonListView.as_view(), name="hackathon-list"),
    path("<hack_id>/team/<team_id>/judging/", views.judging, name="judging"),
]
