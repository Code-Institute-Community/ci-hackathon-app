from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("faq/", views.faq, name="faq"),
    path("judging_criteria/", views.judging_criteria, name="judging_criteria"),
    path("plagiarism_policy/", views.plagiarism_policy, name="plagiarism_policy"),
    path("privacy_policy/", views.privacy_policy, name="privacy_policy"),
    path("useful_resources/", views.useful_resources, name="useful_resources")
]
