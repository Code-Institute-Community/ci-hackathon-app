from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("faq/", views.faq, name="faq"),
    path("judging_criteria/", views.judging_criteria, name="judging_criteria"),
    path("plagiarism_policy/", views.plagiarism_policy, name="plagiarism_policy"),
    path("privacy_policy/", views.privacy_policy, name="privacy_policy"),
    path("post_login/", views.index, name="post_login"),

    path("500/", views.test_500),
    path("404/", views.test_404),
]

