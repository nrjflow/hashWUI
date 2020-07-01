# chat/routing.py
from django.conf.urls import url
import hashcat.consumers.status as status

websocket_urlpatterns = [
    url(r'^ws/task/(?P<task_id>[0-9]+)', status.StatusConsumer),
]