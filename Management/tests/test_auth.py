import pytest
from httpx import AsyncClient
from jose import jwt

from app.core.settings import get_settings
from app.schemas.user import UserCreate, UserRole
from app.services.user_service import UserService

pytestmark = pytest.mark.anyio


async def test_auth_flow(client: AsyncClient, db_session):
    service = UserService()
    user = await service.create(
        db_session,
        UserCreate(
            username="admin",
            password="Str0ng!Pass",
            email="admin@example.com",
            role=UserRole.ADMIN,
        ),
    )

    resp = await client.post(
        "/auth/login",
        json={"username": "admin", "password": "Str0ng!Pass"},
    )
    assert resp.status_code == 200
    tokens = resp.json()
    assert tokens["access_token"]
    assert tokens["refresh_token"]
    settings = get_settings()
    payload = jwt.decode(
        tokens["access_token"],
        settings.secret_key,
        algorithms=["HS256"],
        issuer=settings.jwt_issuer,
        audience=settings.jwt_audience,
    )
    assert payload["iss"] == settings.jwt_issuer
    assert payload["aud"] == settings.jwt_audience
    assert payload.get("jti")
    assert payload.get("iat")

    refresh_payload = jwt.decode(
        tokens["refresh_token"],
        settings.secret_key,
        algorithms=["HS256"],
        issuer=settings.jwt_issuer,
        audience=settings.jwt_audience,
    )
    assert refresh_payload.get("iat")

    refresh = await client.post(
        "/auth/refresh", json={"refresh_token": tokens["refresh_token"]}
    )
    assert refresh.status_code == 200
    new_access = refresh.json()["access_token"]

    headers = {"Authorization": f"Bearer {new_access}"}
    resp2 = await client.get("/users/", headers=headers)
    assert resp2.status_code == 200

    await db_session.commit()
    await db_session.refresh(user)
    assert user.last_login is not None


async def test_protected_endpoint_requires_auth(client: AsyncClient):
    resp = await client.get("/users/")
    assert resp.status_code == 403


async def test_inactive_user_token_forbidden(client: AsyncClient, db_session):
    service = UserService()
    user = await service.create(
        db_session,
        UserCreate(
            username="inactive",
            password="Str0ng!Pass",
            email="inactive@example.com",
            role=UserRole.ADMIN,
        ),
    )

    login = await client.post(
        "/auth/login",
        json={"username": "inactive", "password": "Str0ng!Pass"},
    )
    token = login.json()["access_token"]

    user.is_active = False
    await db_session.commit()

    headers = {"Authorization": f"Bearer {token}"}
    resp = await client.get("/users/", headers=headers)
    assert resp.status_code == 403


async def test_invalid_token_claims_rejected(client: AsyncClient, db_session):
    service = UserService()
    await service.create(
        db_session,
        UserCreate(
            username="claims",
            password="Str0ng!Pass",
            email="c@example.com",
            role=UserRole.ADMIN,
        ),
    )
    login = await client.post(
        "/auth/login",
        json={"username": "claims", "password": "Str0ng!Pass"},
    )
    refresh = login.json()["refresh_token"]
    settings = get_settings()
    payload = jwt.decode(
        refresh,
        settings.secret_key,
        algorithms=["HS256"],
        issuer=settings.jwt_issuer,
        audience=settings.jwt_audience,
    )
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
