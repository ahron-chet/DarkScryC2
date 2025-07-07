import pytest

from app.core.settings import get_settings


def test_settings_require_vars(monkeypatch):
    monkeypatch.delenv("MANAGEMENT_DATABASE_URL", raising=False)
    monkeypatch.delenv("MANAGEMENT_SECRET_KEY", raising=False)
    get_settings.cache_clear()
    with pytest.raises(RuntimeError):
        get_settings()


def test_cors_origins_default(monkeypatch):
    monkeypatch.delenv("MANAGEMENT_CORS_ORIGINS", raising=False)
    get_settings.cache_clear()
    settings = get_settings()
    assert settings.cors_origins == []


def test_cors_origins_parsing(monkeypatch):
    monkeypatch.setenv(
        "MANAGEMENT_CORS_ORIGINS",
        "http://a.com, http://b.com",
    )
    get_settings.cache_clear()
    settings = get_settings()
    assert settings.cors_origins == ["http://a.com", "http://b.com"]
