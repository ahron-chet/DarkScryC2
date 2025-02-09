from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from jwt import PyJWTError

from django.conf import settings
from django.http import HttpRequest

from ninja.errors import HttpError
from ninja.security import HttpBearer

from application.models import User


def jwt_get(token, jwt_secrete, payload_key, default=None):
    """
    Decode and verify a JWT token using project settings, then retrieve a specific claim.

    Returns:
        Claim value or default if not found
    """
    try:
        algorithms = getattr(settings, "JWT_ALGORITHM", ["HS256"])
        if isinstance(algorithms, str):
            algorithms = [algorithms]

        decoded = jwt.decode(
            token,
            key=jwt_secrete,
            algorithms=algorithms
        )
        return decoded.get(payload_key, default)
    except AttributeError as e:
        raise PyJWTError("Missing required JWT configuration in settings") from e
    except PyJWTError as e:
        raise


def create_jwt_token(user_id: UUID) -> str:
    """
    Create a JWT with an 'exp' (expiration) claim
    and a 'sub' (subject) or 'user_id' claim.
    """
    now = datetime.now(tz=timezone.utc)
    exp = now + timedelta(seconds=settings.JWT_EXPIRE_SECONDS)

    payload = {
        "sub": str(user_id),
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


def create_refresh_token(user_id: UUID) -> str:
    """
    Create a long-lived JWT refresh token.
    """
    now = datetime.now(tz=timezone.utc)
    exp = now + timedelta(seconds=settings.JWT_REFRESH_EXPIRE_SECONDS)
    
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": exp,
        "scope": "refresh_token"
    }
    
    return jwt.encode(
        payload, 
        settings.JWT_REFRESH_SECRET, 
        algorithm=settings.JWT_ALGORITHM
    )

    
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