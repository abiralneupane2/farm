from . import consumer
from django.urls import path
ws_urlpatterns = [
    path('ws/graph/', consumer.ClientConsumer()),
    path('ws/data/', consumer.DeviceConsumer()),
]