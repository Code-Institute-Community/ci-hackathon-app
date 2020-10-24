from django.urls import path
from . import views

urlpatterns = [
    path("", views.resources, name="resources"),
    path('add/', views.add_resource, name='add_resource'),

]
