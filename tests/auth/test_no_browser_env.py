"""WORKSPACE_MCP_NO_BROWSER keeps the OAuth consent URL out of the local default browser."""

import pytest

import auth.google_auth as google_auth


@pytest.fixture(autouse=True)
def _legacy_stdio(monkeypatch):
    monkeypatch.setattr(google_auth, "get_transport_mode", lambda: "stdio")
    monkeypatch.setattr(google_auth, "is_oauth21_enabled", lambda: False)
    monkeypatch.delenv("WORKSPACE_MCP_NO_BROWSER", raising=False)


def test_legacy_stdio_opens_browser_by_default():
    assert google_auth._should_auto_open_browser() is True


@pytest.mark.parametrize("value", ["1", "true", "TRUE", "yes", " True "])
def test_no_browser_env_disables_auto_open(monkeypatch, value):
    monkeypatch.setenv("WORKSPACE_MCP_NO_BROWSER", value)
    assert google_auth._should_auto_open_browser() is False


@pytest.mark.parametrize("value", ["", "0", "false", "no"])
def test_no_browser_env_falsy_values_keep_auto_open(monkeypatch, value):
    monkeypatch.setenv("WORKSPACE_MCP_NO_BROWSER", value)
    assert google_auth._should_auto_open_browser() is True


def test_never_opens_outside_legacy_stdio(monkeypatch):
    monkeypatch.setattr(google_auth, "get_transport_mode", lambda: "streamable-http")
    assert google_auth._should_auto_open_browser() is False

    monkeypatch.setattr(google_auth, "get_transport_mode", lambda: "stdio")
    monkeypatch.setattr(google_auth, "is_oauth21_enabled", lambda: True)
    assert google_auth._should_auto_open_browser() is False
