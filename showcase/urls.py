from django.urls import path
from .views import showcase

urlpatterns = [
    path("", showcase, name="showcase"),
]
