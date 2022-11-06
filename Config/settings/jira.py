from .base import *  # noqa
from dotenv import load_dotenv

if env('CURRENT_ENV') == "jira":
    jira_dotenv_path = os.path.join(BASE_DIR, 'environments/jira/.env')
    load_dotenv(jira_dotenv_path)

DEBUG = True


ALLOWED_HOSTS = [
                'localhost',
                '127.0.0.1',
                'gruffalo.io',
                'ajishra.herokuapp.com',
                '8712-5-180-208-246.ngrok.io'
                ]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'options': '-c search_path=' + env('DB_SCHEMA')
        },
        'NAME': env('DB'),
        'USER': env("DB_USER"),
        'PASSWORD': env("DB_PASS"),
        'HOST': env("DB_HOST"),
        'PORT': '5432',
    },
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": BASE_DIR / "jira_db.sqlite3",
    # },
        'jira': {
            'ENGINE': 'django_atlassian.backends.jira',
            'NAME': 'https://' + env('JIRA_SITE') + "." + env('JIRA_DOMAIN'),
            'USER': env('JIRA_API_USER'),
            'PASSWORD': env('JIRA_API_TOKEN'),
            'SECURITY': '',
                }
        }

DATABASE_ROUTERS = ['Leia_atlassian.router.Router']

APPEND_SLASH = False