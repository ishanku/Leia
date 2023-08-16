import environ
from Config.basepath import *

env = environ.Env()
print("::::::::::::::::" + env("REDIS_URL") + "***************")

CACHES = {
    'default': {
        # 'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        "BACKEND": "django_redis.cache.RedisCache",
        'LOCATION': 'redis://default:' + env("REDIS_PASSWORD") + '@' + env('REDIS_URL'),
        "TIMEOUT": 60000,
        "PICKLE_VERSION": 2,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'SOCKET_TIMEOUT': 60,
            # 'SOCKET_CONNECT_TIMEOUT': 5,
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 50,
                'timeout': 60,
            },
            'SERIALIZER_CLASS': 'redis_cache.serializers.PickleSerializer',
            'SERIALIZER_CLASS_KWARGS': {
                'pickle_version': -2
            },
            # 'COMPRESSOR_CLASS': 'redis_cache.compressors.BZip2Compressor',
            'COMPRESSOR_CLASS': 'redis_cache.compressors.ZLibCompressor',
            'COMPRESSOR_CLASS_KWARGS': {
                'level': 5,  # 0 - 9; 0 - no compression; 1 - fastest, biggest; 9 - slowest, smallest
            },
        }
    },
    "FileCache": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "FileCache/Django/",
    }
}
# CACHE_TTL = 60 * 15

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#         'LOCATION': 'jira_cache_table',
#     }
# }
#
# CACHES = {
#     "FileCache": {
#         "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
#         "LOCATION": "FileCache/Django/",
#     }
# }