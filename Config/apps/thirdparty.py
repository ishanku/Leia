from django.conf import settings

THIRD_PARTY_APPS = [
                "crispy_forms",
                "corsheaders",
              #  'Atlassian',
                ]
if settings.SOCIALACCOUNT_ENABLED:
    THIRD_PARTY_APPS += [
                                "allauth",
                                "allauth.account",
                                "allauth.socialaccount",
                                'allauth.socialaccount.providers.google',
                        ]