from django.urls import path

from .views import HackathonListView, HackathonDetailView, ajax_enroll_toggle

urlpatterns = [
    path('', HackathonListView.as_view(), name="hackathon-list"),
    path('<int:pk>/',
         HackathonDetailView.as_view(), name='hackathon-detail'),
    path('ajax/enroll/', ajax_enroll_toggle, name='enroll-toggle')
]
