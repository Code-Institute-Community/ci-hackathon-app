from django.urls import path

from .views import HackathonListView, create_hackathon

urlpatterns = [
    path('', HackathonListView.as_view(), name='hackathon-list'),
    path("create_hackathon", create_hackathon, name='create_hackathon')
]
