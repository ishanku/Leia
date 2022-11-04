from django.urls import path, include

from Roja import views


app_name = "Roja"

urlpatterns = [
    path("", views.index.as_view()),
    path("index.html", views.index.as_view()),
    path("users/", include("Roja.users.urls", namespace="Roja.users")),
    path("atlassian/", include('Leia_atlassian.urls', namespace='Leia_atlassian')),
    path("jira/", include('Integration.jira.urls', namespace='integration.jira')),

]