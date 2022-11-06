from django.urls import path, include

from Roja import views


app_name = "Roja"

urlpatterns = [
    path("", views.index),
    path("index.html", views.index),
    path("users/", include("Roja.users.urls", namespace="Roja.users")),
    path("atlassian/", include('Leia_atlassian.urls', namespace='Leia_atlassian')),
    path("jira/", include('Integration.jira.urls', namespace='integration.jira')),
    path("Jira/", include('Integration.jira.urls', namespace='integration.jira')),

]