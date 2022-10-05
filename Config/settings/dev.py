from .base import *  # noqa
from dotenv import load_dotenv

if env('CURRENT_ENV') == "dev":
    dev_dotenv_path = os.path.join(BASE_DIR, 'environments/dev/.env')
    load_dotenv(dev_dotenv_path)

DEBUG = True


ALLOWED_HOSTS = [
                'localhost',
                '127.0.0.1',
                'gruffalo.io',
                'ajishra.herokuapp.com'
                ]

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'OPTIONS': {
#             'options': '-c search_path=' + env('DB_USER')
#         },
#         'NAME': env('DB'),
#         'USER': env("DB_USER"),
#         'PASSWORD': env("DB_PASS"),
#         'HOST': env("DB_HOST"),
#         'PORT': '5432',
#     }
# }