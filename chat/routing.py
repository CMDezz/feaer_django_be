from django.urls import path
from . import consumers
from django.urls import re_path


# websocket_urlpatterns = [
#     path('chat/', consumers.ChatConsumer.as_asgi()),
# ]
websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    re_path(r"ws/chat/", consumers.ChatConsumer.as_asgi()),
]