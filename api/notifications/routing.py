# from django.conf.urls import url
# from django.urls import re_path
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator
# from api.notifications import consumers

# application = ProtocolTypeRouter({
#     'websocket' : AllowedHostsOriginValidator(
#         AuthMiddlewareStack(
#             URLRouter(
#                 [
#                     url(r"^notifications/", consumers.NotificationConsumer)
#                 ]
#             )
#         )
#     )
# })

# # websocket_urlpatterns = [
# #     re_path(r'ws/notification/$', consumers.NotificationConsumer.as_asgi()),

# # ]