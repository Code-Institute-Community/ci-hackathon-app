from django.urls import path
from .views import view_showcases, view_showcase

urlpatterns = [
    path("", view_showcases, name="view_showcases"),
    path("<int:showcase_id>/", view_showcase, name="view_showcase"),
]
