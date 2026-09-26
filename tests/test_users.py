"""ReqRes /users contract tests — status code + JSON schema + semantics."""
from __future__ import annotations

import time
from datetime import datetime
from typing import Any

import pytest

from schemas import (
    CREATE_USER_SCHEMA,
    SINGLE_USER_SCHEMA,
    UPDATE_USER_SCHEMA,
    USER_LIST_SCHEMA,
)


def _assert_iso8601(value: str) -> None:
    datetime.fromisoformat(value.replace("Z", "+00:00"))


@pytest.mark.users
@pytest.mark.smoke
@pytest.mark.regression
def test_list_users_page_two(client: Any, validate_schema: Any) -> None:
    resp = client.get("/users", params={"page": 2})
    assert resp.status_code == 200, resp.text
    body = resp.json()
    validate_schema(body, USER_LIST_SCHEMA)
    assert body["page"] == 2
    assert body["data"], "page 2 should contain at least one user"
    assert len(body["data"]) <= body["per_page"]
    for user in body["data"]:
        assert "@" in user["email"]


@pytest.mark.users
@pytest.mark.smoke
@pytest.mark.regression
def test_get_single_user(client: Any, validate_schema: Any) -> None:
    resp = client.get("/users/2")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    validate_schema(body, SINGLE_USER_SCHEMA)
    data = body["data"]
    assert data["id"] == 2
    assert "@" in data["email"] and "." in data["email"]
    assert data["avatar"].startswith("http")


@pytest.mark.users
@pytest.mark.regression
@pytest.mark.negative
def test_get_missing_user_returns_404(client: Any) -> None:
    resp = client.get("/users/23")
    assert resp.status_code == 404, resp.text
    assert resp.json() == {}


@pytest.mark.users
@pytest.mark.smoke
@pytest.mark.regression
def test_create_user(client: Any, validate_schema: Any) -> None:
    payload = {"name": "morpheus", "job": "leader"}
    resp = client.post("/users", json=payload)
    assert resp.status_code == 201, resp.text
    body = resp.json()
    validate_schema(body, CREATE_USER_SCHEMA)
    assert body["name"] == payload["name"]
    assert body["job"] == payload["job"]
    assert body["id"]
    _assert_iso8601(body["createdAt"])


@pytest.mark.users
@pytest.mark.regression
def test_update_user_put(client: Any, validate_schema: Any) -> None:
    payload = {"name": "morpheus", "job": "zion resident"}
    resp = client.put("/users/2", json=payload)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    validate_schema(body, UPDATE_USER_SCHEMA)
    assert body["name"] == payload["name"]
    assert body["job"] == payload["job"]
    _assert_iso8601(body["updatedAt"])


@pytest.mark.users
@pytest.mark.regression
def test_update_user_patch(client: Any, validate_schema: Any) -> None:
    payload = {"job": "captain"}
    resp = client.patch("/users/2", json=payload)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    validate_schema(body, UPDATE_USER_SCHEMA)
    assert body["job"] == payload["job"]
    _assert_iso8601(body["updatedAt"])


@pytest.mark.users
@pytest.mark.regression
def test_delete_user(client: Any) -> None:
    resp = client.delete("/users/2")
    assert resp.status_code == 204, resp.text
    assert resp.content == b""


@pytest.mark.users
@pytest.mark.regression
def test_delayed_response_still_valid(client: Any, validate_schema: Any) -> None:
    start = time.monotonic()
    resp = client.get("/users", params={"delay": 3})
    elapsed = time.monotonic() - start
    assert resp.status_code == 200, resp.text
    validate_schema(resp.json(), USER_LIST_SCHEMA)
    assert elapsed >= 2.5, f"delay=3 should slow the response (took {elapsed:.1f}s)"
