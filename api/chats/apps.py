from django.apps import AppConfig


class ChatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # This makes sure Django detects the app correctly due to the folder structure.
    name = 'api.chats'
