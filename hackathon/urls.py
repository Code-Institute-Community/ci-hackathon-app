from django.urls import path

from .views import HackathonListView, HackathonDetailView

urlpatterns = [
    path('', HackathonListView.as_view(), name="hackathon-list"),
    path('<int:pk>/',
         HackathonDetailView.as_view(), name='hackathon-detail'),
]
