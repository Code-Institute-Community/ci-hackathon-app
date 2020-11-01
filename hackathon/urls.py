from django.urls import path
from .views import (
    HackathonListView,
    create_hackathon,
    update_hackathon,
    delete_hackathon,
    HackathonDetailView,
    enroll_toggle,
    judging
)

urlpatterns = [
    path('', HackathonListView.as_view(), name="hackathon-list"),
    path("<int:hack_id>/team/<int:team_id>/judging/", judging, name="judging"),
    path("create_hackathon", create_hackathon, name='create_hackathon'),
    path("<int:hackathon_id>/update_hackathon", update_hackathon, name="update_hackathon"),
    path("<int:hackathon_id>/delete_hackathon", delete_hackathon, name="delete_hackathon"),
    path('<int:pk>/',
         HackathonDetailView.as_view(), name='hackathon_detail'),
    path('enroll', enroll_toggle, name='enroll_toggle')
]

