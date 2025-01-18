import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from ninja.security import HttpBearer
from ninja.errors import HttpError
from django.http import HttpRequest
from application.models import User

def create_jwt_token(user_id: int) -> str:
    """
    Create a JWT with an 'exp' (expiration) claim
    and a 'sub' (subject) or 'user_id' claim.
    """
    now = datetime.now(tz=timezone.utc)
    exp = now + timedelta(seconds=settings.JWT_EXPIRE_SECONDS)

    payload = {
        "sub": user_id,
        "iat": now,
        "exp": exp
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token

def decode_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise
    except jwt.InvalidTokenError:
        raise



    
class TokenAuth(HttpBearer):

    async def __call__(self, request: HttpRequest):
        user = await request.auser()
        if user.is_authenticated:
            return user 
        headers = request.headers
        auth_value = headers.get(self.header)
        if not auth_value:
            return None
        parts = auth_value.split(" ")

        if parts[0].lower() != self.openapi_scheme:
            if settings.DEBUG:
                # logger.error(f"Unexpected auth - '{auth_value}'")
                return None
        token = " ".join(parts[1:])
        return await self.authenticate(request, token)
    
    async def authenticate(self, request:HttpRequest, token, *args, **kwargs):
        try:
            payload = decode_jwt_token(token)
        except jwt.ExpiredSignatureError:
            raise HttpError(401, "Token expired")
        except jwt.InvalidTokenError:
            raise HttpError(401, "Invalid token")

        user_id = payload.get("sub")
        if not user_id:
            raise HttpError(401, "Invalid payload")

        user = await User.objects.filter(user_id=user_id).afirst()
        if not user:
            raise HttpError(401, "User not found")
        request._api_user = user
        return user