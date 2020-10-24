from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("home.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("profile/", include("profiles.urls")),
    path("resources/", include("resources.urls")),
    path("hackathon/", include(("hackathon.urls", "hackathon"),
                               namespace='hackathon')),
    path("submission/", include("submissions.urls")),
]
