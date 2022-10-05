from Config.basesettings import *

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.forms",
]

if SOCIALACCOUNT_ENABLED:
    INSTALLED_APPS += [ 'django.contrib.sites' ]