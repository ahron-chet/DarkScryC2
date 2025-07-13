import pytest
from app.core.settings import get_app_settings
from app.models.user import UserRole
from httpx import AsyncClient
from jose import jwt

pytestmark = pytest.mark.anyio


def _decode(token: str) -> dict:
    settings = get_app_settings()
    return jwt.decode(
        token,
        settings.secret_key,
        algorithms=["HS256"],
        issuer=settings.jwt_issuer,
        audience=settings.jwt_audience,
    )


async def test_login_returns_tokens(client: AsyncClient, create_test_user, get_token):
    await create_test_user("admin", UserRole.ADMIN)
    token = await get_token("admin")
    payload = _decode(token)
    assert payload["iss"] == get_app_settings().jwt_issuer


async def test_refresh_flow(client: AsyncClient, create_test_user):
    await create_test_user("admin", UserRole.ADMIN)
    login = await client.post(
        "/auth/login", json={"username": "admin", "password": "Str0ng!Pass"}
    )
    refresh = login.json()["refresh_token"]
    resp = await client.post("/auth/refresh", json={"refresh_token": refresh})
    assert resp.status_code == 200
    new_token = resp.json()["access_token"]
    assert _decode(new_token)


async def test_last_login_set(client: AsyncClient, create_test_user, db_session):
    user = await create_test_user("admin", UserRole.ADMIN)
    await client.post(
        "/auth/login", json={"username": "admin", "password": "Str0ng!Pass"}
    )
    await db_session.commit()
    await db_session.refresh(user)
    assert user.last_login is not None


async def test_protected_endpoint_requires_auth(client: AsyncClient):
    resp = await client.get("/users/")
    assert resp.status_code == 403


async def test_inactive_user_token_forbidden(
    client: AsyncClient, create_test_user, get_token, db_session
):
    user = await create_test_user("inactive", UserRole.ADMIN)
    token = await get_token("inactive")
    user.is_active = False
    await db_session.commit()
    headers = {"Authorization": f"Bearer {token}"}
    resp = await client.get("/users/", headers=headers)
    assert resp.status_code == 403


async def test_invalid_token_claims_rejected(
    client: AsyncClient, create_test_user, get_token
):
    await create_test_user("claims", UserRole.ADMIN)
    login = await client.post(
        "/auth/login", json={"username": "claims", "password": "Str0ng!Pass"}
    )
    refresh = login.json()["refresh_token"]
    settings = get_app_settings()
    payload = _decode(refresh)
    payload["aud"] = "bad-aud"
    bad_token = jwt.encode(payload, settings.secret_key, algorithm="HS256")
    resp = await client.post("/auth/refresh", json={"refresh_token": bad_token})
    assert resp.status_code == 401

    payload["aud"] = settings.jwt_audience
    payload["iss"] = "bad-iss"
    bad_access = jwt.encode(payload, settings.secret_key, algorithm="HS256")
    headers = {"Authorization": f"Bearer {bad_access}"}
    resp2 = await client.get("/users/", headers=headers)
    assert resp2.status_code == 401
