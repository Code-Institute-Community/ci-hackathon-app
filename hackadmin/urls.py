from django.urls import path
from .views import (
    hackadmin_panel,
    hackathon_stats,
)

urlpatterns = [
    path('', hackadmin_panel, name='hackadmin_panel'),
    path('stats/', hackathon_stats, name='hackathon_stats'),
]
