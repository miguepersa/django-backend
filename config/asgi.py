"""
ASGI config for api project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import sys
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent

# If DJANGO_SETTINGS_MODULE is unset, default to the local settings - config.settings.local
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# This allows easy placement of apps within the interior
# api directory.

sys.path.append(str(ROOT_DIR / "api"))

from channels.routing import ProtocolTypeRouter, URLRouter  # noqa isort:skip
from django.core.asgi import get_asgi_application



# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.

django_asgi_app = get_asgi_application()

from api.chats.middleware import TokenAuthMiddleware
from channels.auth import AuthMiddlewareStack

# from channels.layers import get_channel_layer
# channel_layer = get_channel_layer()

# Set the environment variable ASGI_THREADS to a number of threads lower than your connections limit on your .asgi file or on heroku site -> settings -> configVars. If you are using daphne, the default threads are CPU cores * 5, each thread with a connection.
# os.environ['ASGI_THREADS']="4"


# Import websocket application here, so apps from django_application are loaded first

from config import routing  # noqa isort:skip


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": TokenAuthMiddleware(
            URLRouter(routing.websocket_urlpatterns)
        ),
    }
)
