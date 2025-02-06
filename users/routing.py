from django.urls import path
from .consumers import selectTranscriptConsumer

websocket_urlpatterns = [
    path("register/profile/ws/listen/", selectTranscriptConsumer().as_asgi()),
]
