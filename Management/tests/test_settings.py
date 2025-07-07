import pytest

from app.core.settings import get_settings


def test_settings_require_vars(monkeypatch):
    monkeypatch.delenv("MANAGEMENT_DATABASE_URL", raising=False)
    monkeypatch.delenv("MANAGEMENT_SECRET_KEY", raising=False)
    get_settings.cache_clear()
    with pytest.raises(RuntimeError):
        get_settings()
