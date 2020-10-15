from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("criteria/", views.criteria, name="criteria"),
]
