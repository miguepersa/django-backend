# This is the settings file that you use when you’re working on the project locally. Lo- cal development-specific settings include DEBUG mode, log level, and activation of developer tools like django-debug-toolbar.

# To start the Python interactive interpreter with Django, using your settings/local.py settings file:
#   python manage.py shell --settings=config.settings.local

# To run the local development server with your settings/local.py settings file:
# python manage.py runserver --settings=config.settings.local

# Sometimes called development.py

# SECURITY WARNING: don't run with debug turned on in production!

# You should remember to add settings\development.py to .gitignore, when deploying using a version control system.

from .base import *

DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar',
]

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [
                       s.strip() for s in v.split(',')])

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    },
}

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = config('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = True


DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '',
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(config("REDIS_HOST"), int(config("REDIS_PORT")))],
            "symmetric_encryption_keys": [config("SECRET_KEY")],
        },
    },
}

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]
