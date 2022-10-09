# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from Leia_atlassian.models.connect import SecurityContext

class SecurityContextAdmin(admin.ModelAdmin):
    list_display = ['key']

admin.site.register(SecurityContext, SecurityContextAdmin)
