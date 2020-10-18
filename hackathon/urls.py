from django.urls import path
from . import views

urlpatterns = [
    path("", views.judging, name="judging")
]
