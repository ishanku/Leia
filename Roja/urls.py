from django.urls import path, include

from Roja import views

app_name = "Roja"

urlpatterns = [
    path("", views.index),
    path("index.html", views.index),
    path("users/", include("Roja.users.urls", namespace="users")),
   # path("atlassian/", include('django_atlassian.urls')),
    path("jira/", include('Integration.jira.urls')),
    path("accounts/", include("allauth.urls")),
]