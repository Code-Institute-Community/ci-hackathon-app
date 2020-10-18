from django.urls import path
from . import views
from .views import HackathonListView

urlpatterns = [
    path('', HackathonListView.as_view(), name="hackathon-list"),
    path("judging/", views.judging, name="judging"),
]
