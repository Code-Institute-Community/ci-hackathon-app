from django.urls import path
from . import views

urlpatterns = [
    path("judging/", views.judging, name="judging")
]
