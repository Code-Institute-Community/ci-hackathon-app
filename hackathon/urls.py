from django.urls import path

from .views import HackathonListView

urlpatterns = [
    path('', HackathonListView.as_view(), name="hackathon-list")
]
