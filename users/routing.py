from django.urls import path
from Text2Speech.consumers import select_transcript_consumer

websocket_urlpatterns = [
    path("register/profile/ws/listen/", select_transcript_consumer().as_asgi()),
]
