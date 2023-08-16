from django.conf import settings

DECIMAL_PLACES = getattr(settings, "CURRENCY_DECIMAL_PLACES", 2)
BASE_CURRENCY = getattr(settings, "BASE_CURRENCY", "USD")
MAX_CURRENCY_LENGTH = 15

# Decimal separator symbol
DECIMAL_SEPARATOR = "."

# Thousand separator symbol
THOUSAND_SEPARATOR = ","

# Boolean that sets whether to add thousand separator when formatting numbers
USE_THOUSAND_SEPARATOR = False
