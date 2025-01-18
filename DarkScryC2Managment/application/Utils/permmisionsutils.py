# permissions.py
from functools import wraps
from ninja.errors import HttpError


def check_permissions(permissions: list[str]):
    def decorator(func):
        @wraps(func)
        async def wrapper(request, *args, **kwargs):
            _api_user = getattr(request, "_api_user", None)
            if _api_user:
                user = _api_user
            else:
                user = await request.auser()
            for perm in permissions:
                has_permission = await user.ahas_perm(perm)
                if not has_permission:
                    raise HttpError(403, f"Forbidden: missing '{perm}' permission")
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator
