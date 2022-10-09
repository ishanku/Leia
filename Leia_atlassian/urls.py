# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import path, include
from Leia_atlassian import views

urlpatterns = [
    path(r'^installed/$', views.installed, name='Atlassian-installed'),
    path("installed/", views.installed, name='Atlassian-installed'),
]

