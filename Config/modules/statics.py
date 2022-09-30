from Config.basepath import *
import os

STATIC_ROOT = os.path.join(BASE_DIR, 'dock/static')
STATIC_URL = "/static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'Roja/static'),
    os.path.join(BASE_DIR, 'Integration/static'),
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

MEDIA_ROOT = os.path.join(BASE_DIR, "dock/media")
MEDIA_URL = "/media/"


