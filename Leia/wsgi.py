"""
WSGI config for Leia project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
from Config.modules.environment import *
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "Config.settings." + env('CURRENT_ENV'))

application = get_wsgi_application()
