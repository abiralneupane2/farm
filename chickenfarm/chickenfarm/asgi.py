# mysite/asgi.py
import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

from main.routing import ws_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chickenfarm.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(URLRouter(ws_urlpatterns))
    # Just HTTP for now. (We can add other protocols later.)
})