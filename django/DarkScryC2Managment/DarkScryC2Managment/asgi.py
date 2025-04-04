"""
ASGI config for DarkScryC2Managment project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
import django
from .middleware import WSAuthMiddleware


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DarkScryC2Managment.settings')

django.setup()

from application.urls.api_urls import urlpatterns_webSocket

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        WSAuthMiddleware(
            URLRouter(urlpatterns_webSocket)
        )
    )
})
