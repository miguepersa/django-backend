# Settings for running tests including test runners, in-memory database definitions, and log settings.

from .base import *

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3'
}
    
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
    