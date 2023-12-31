from .base import *  # noqa
from dotenv import load_dotenv

if env('CURRENT_ENV') == "dev":
    dev_dotenv_path = os.path.join(BASE_DIR, 'environments/dev/.env')
    load_dotenv(dev_dotenv_path)

buildPath = 'environment/'  + env('CURRENT_ENV') + '.env'
load_dotenv(os.path.join(BASE_DIR, buildPath))

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
    }
}