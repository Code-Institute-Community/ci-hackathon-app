from django.urls import path

from .views import HackathonListView, create_event

urlpatterns = [
    path('', HackathonListView.as_view(), name="hackathon-list"),
    path("create-event", create_event, name="create_event")
]
