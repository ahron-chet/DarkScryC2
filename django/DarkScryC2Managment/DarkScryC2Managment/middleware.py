from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser
from application.Utils.jwtutils import jwt_get
from .settings import JWT_SECRET
from application.models import User


class WSAuthMiddleware:
    """
    Simple ASGI middleware that authenticates WebSocket connections with JWT from query string
    """
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = scope['query_string'].decode()
        query_params = parse_qs(query_string)
        token = query_params.get('token', [None])[0]  # get first 'token' param or None

        if token:
            try:
                user_id = jwt_get(
                    jwt_secrete=JWT_SECRET,
                    token=token,
                    payload_key="sub"
                )
                user =  await User.objects.filter(user_id=user_id).afirst()
                scope['user'] = user
            except :
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()

        # Continue to the next middleware or consumer
        return await self.inner(scope, receive, send)
