from django.conf import settings

DECIMAL_PLACES = getattr(settings, "CURRENCY_DECIMAL_PLACES", 2)
BASE_CURRENCY = getattr(settings, "BASE_CURRENCY", "USD")
MAX_CURRENCY_LENGTH = 15
