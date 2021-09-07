from django.urls import path
from .views import view_showcases, view_showcase
from images.views import render_image

urlpatterns = [
    path("", view_showcases, name="view_showcases"),
    path("<int:showcase_id>/", view_showcase, name="view_showcase"),
    path("<int:showcase_id>/image/<str:image_hash>/", render_image,
         name="render_showcase_image"),
]
