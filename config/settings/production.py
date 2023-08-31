# This is the settings file used by your live production server(s). That is, the server(s) that host the real live website. This file con- tains production-level settings only.

import ssl
from .base import *
import dj_database_url

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

# INSTALLED_APPS.append('cloudinary_storage',
#                       'cloudinary')

ALLOWED_HOSTS = ['tecnikids-back.herokuapp.com', "127.0.0.1"]

CSRF_TRUSTED_ORIGINS = ['https://*.tecnikids-back.herokuapp.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}

db_from_env = dj_database_url.config(
    conn_max_age=0, ssl_require=True, conn_health_checks=True,)
# db_from_env = dj_database_url.config(ssl_require=True)


ssl_context = ssl.SSLContext()
ssl_context.check_hostname = False

heroku_redis_ssl_host = {
    'address': os.environ.get('REDIS_URL'),
    'ssl': ssl_context
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': (heroku_redis_ssl_host,),
            "symmetric_encryption_keys": [SECRET_KEY],
        }
    },
}


# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
#             "symmetric_encryption_keys": [SECRET_KEY],
#         },
#     },
# }


DATABASES["default"] = db_from_env

ASGI_THREADS = os.environ.get('ASGI_THREADS')

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:11211',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

# EMAIL CONFIG

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

# TLS Settings

# CORS_REPLACE_HTTPS_REFERER      = True
# HOST_SCHEME                     = "https://"
# SECURE_PROXY_SSL_HEADER         = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT             = True
# SESSION_COOKIE_SECURE           = True
# CSRF_COOKIE_SECURE              = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
# SECURE_HSTS_SECONDS             = 1000000
# SECURE_FRAME_DENY               = True


# TLS Redis - Heroku
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.redis.RedisCache",
#         "LOCATION": os.environ.get('REDIS_TLS_URL'),
#         "OPTIONS": {
#             "ssl_cert_reqs": None
#         }
#     }
# }

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # "CONNECTION_POOL_KWARGS": {
            #     "ssl_params": {
            #         "ssl_version": ssl.PROTOCOL_TLS,
            #         "ssl_cert_reqs": ssl.CERT_NONE,  # Use this to disable certificate checks
            #     }
            # },
        },
    }
}
