from Config.basesettings import *

THIRD_PARTY_APPS = [
                "crispy_forms",
                "corsheaders",
                ]

if SOCIALACCOUNT_ENABLED:
    THIRD_PARTY_APPS += [
                                "allauth",
                                "allauth.account",
                                "allauth.socialaccount",
                                'allauth.socialaccount.providers.google',
                        ]