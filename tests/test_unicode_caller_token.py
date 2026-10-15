import pytest

from opencode_go_proxy.errors import ProxyError
from opencode_go_proxy.guards import (
    CALLER_TOKEN_ENV,
    CALLER_TOKEN_HEADER,
    REMOTE_ENV,
    check_client,
)


def test_nonascii_supplied_token_is_rejected_instead_of_crashing(monkeypatch):
    monkeypatch.setenv(REMOTE_ENV, "1")
    monkeypatch.setenv(CALLER_TOKEN_ENV, "a" * 32)
    with pytest.raises(ProxyError) as error:
        check_client("192.0.2.1", {CALLER_TOKEN_HEADER: "é" * 32})
    assert error.value.status == 401


def test_configured_unicode_token_can_be_compared(monkeypatch):
    monkeypatch.setenv(REMOTE_ENV, "1")
    monkeypatch.setenv(CALLER_TOKEN_ENV, "é" * 32)
    check_client("192.0.2.1", {CALLER_TOKEN_HEADER: "é" * 32})
