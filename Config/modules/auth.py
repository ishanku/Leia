from Config.basesettings import *

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

if SOCIALACCOUNT_ENABLED:
    from Config.modules.social import *
    AUTHENTICATION_BACKENDS += ['allauth.account.auth_backends.AuthenticationBackend']
    #Migration Modules
    MIGRATION_MODULES = {"sites": "Config.contrib.sites.migrations"}
    SITE_ID = 1
    #More for social auth
    AUTHENTICATION_BACKENDS += [ "allauth.account.auth_backends.AuthenticationBackend"]
    AUTH_USER_MODEL = "users.User"
    LOGIN_REDIRECT_URL = "users:redirect"
    LOGIN_URL = "account_login"

# PASSWORDS
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]



if SOCIALACCOUNT_ENABLED:
    ACCOUNT_ALLOW_REGISTRATION = True  # env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
    ACCOUNT_AUTHENTICATION_METHOD = "username"
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_EMAIL_VERIFICATION = "mandatory"
    ACCOUNT_ADAPTER = "Roja.users.adapters.AccountAdapter"
    SOCIALACCOUNT_ADAPTER = "Roja.users.adapters.SocialAccountAdapter"

    SOCIALACCOUNT_QUERY_EMAIL = True
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'