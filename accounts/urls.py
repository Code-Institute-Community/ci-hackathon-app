from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path('external/', LoginView.as_view()),
]
