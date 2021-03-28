from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("home.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("custom_slack_provider.urls")),
    path("images/", include("images.urls")),
    path("profile/", include("profiles.urls")),
    path("resources/", include("resources.urls")),
    path("hackadmin/", include(("hackadmin.urls", "hackadmin"),
                               namespace='hackadmin')),
    path("hackathon/", include(("hackathon.urls", "hackathon"),
                               namespace='hackathon')),
    path("showcase/", include("showcase.urls")),
    path("submission/", include("submissions.urls")),
    path("teams/", include("teams.urls")),
]
