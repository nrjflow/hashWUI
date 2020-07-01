from channels.routing import ProtocolTypeRouter, URLRouter
import hashcat.routing

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': URLRouter(
        hashcat.routing.websocket_urlpatterns
    ),
})