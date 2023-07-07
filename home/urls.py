from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("faq/", views.faq, name="faq"),
    path('codeofconduct/', views.codeofconduct, name="codeofconduct"),   
    path("plagiarism_policy/", views.plagiarism_policy,
         name="plagiarism_policy"),
    path("privacy_policy/", views.privacy_policy, name="privacy_policy"),
    path("post_login/", views.index, name="post_login"),

    path("save_partnership_contact_form/", views.save_partnership_contact_form,
         name="save_partnership_contact_form"),
    path("500/", views.test_500),
    path("404/", views.test_404),
    
]
