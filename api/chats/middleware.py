import jwt, re
import traceback
from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser
from django.conf import LazySettings
from channels.db import database_sync_to_async
from jwt import InvalidSignatureError, ExpiredSignatureError, DecodeError
from urllib import parse
from django.contrib.auth import  get_user_model

User = get_user_model() 

settings = LazySettings()

@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware:
    def __init__(self, app):
        # Store the ASGI application we were passed`
        self.app = app

    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        # scope['user'] = await get_user(int(scope["query_string"]))
        try:
            query = parse.parse_qs(scope['query_string'].decode("utf-8"))['token'][0]
            if query:
                try:
                    user_jwt = jwt.decode(
                        query,
                        settings.SECRET_KEY,
                        algorithms="HS256"
                    )
                    scope["token"] = query

                    scope['user'] = await get_user(user_jwt['user_id'])

                except (InvalidSignatureError, KeyError, ExpiredSignatureError, DecodeError):
                    traceback.print_exc()
                    pass

                except Exception as e:
                    traceback.print_exc(e)
            # print(scope["user"])
            return await self.app(scope, receive, send)
        except:
            scope['user']=AnonymousUser()
            return  await self.app(scope, receive, send)

TokenAuthMiddlewareStack = lambda app: TokenAuthMiddleware(AuthMiddlewareStack(app))