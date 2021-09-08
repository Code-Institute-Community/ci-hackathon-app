from django.urls import path
from . import views

urlpatterns = [
    path("", views.resources, name="resources"),
    path('add/', views.add_resource, name='add_resource'),
    path('delete/<int:resource_id>/', views.delete_resource,
         name='delete_resource'),
    path('edit/<int:resource_id>/', views.edit_resource, name='edit_resource'),
]
