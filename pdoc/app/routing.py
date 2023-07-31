from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/video-calling/<slug:slug>', consumers.Prescribe.as_asgi())
]