from django.urls import path
from .consumers import TranscriptConsumer

websocket_urlpatterns = [
    path('register/profile/ws/listen/', TranscriptConsumer.as_asgi()),
]
