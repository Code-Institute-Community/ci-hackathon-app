from django.urls import path

from .views import save_image

urlpatterns = [
    path("", save_image, name="save_image")
]
