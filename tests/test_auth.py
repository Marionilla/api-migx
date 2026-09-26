from __future__ import annotations

from typing import Any

import pytest

from schemas import (
    REGISTER_SUCCESS_SCHEMA,
    LOGIN_SUCCESS_SCHEMA,
    ERROR_SCHEMA,
)


@pytest.mark.auth
@pytest.mark.smoke
@pytest.mark.regression
def test_register_success(client: Any, validate_schema: Any) -> None:
    resp = client.post(
        "/register", json={"email": "eve.holt@reqres.in", "password": "pistol"}
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    validate_schema(body, REGISTER_SUCCESS_SCHEMA)
    assert isinstance(body["id"], int)
    assert body["token"]
    
    
@pytest.mark.auth
@pytest.mark.regression
@pytest.mark.negative
def test_register_missing_password(client: Any, validate_schema: Any) -> None:
    resp = client.post("/register", json={"email": "sydney@fife"})
    assert resp.status_code == 400, resp.text
    validate_schema(resp.json(), ERROR_SCHEMA)
    
    
@pytest.mark.auth
@pytest.mark.regression
@pytest.mark.negative
def test_register_missing_fields(client: Any, validate_schema: Any) -> None:
    resp = client.post("/register", json={})
    assert resp.status_code == 400, resp.text
    validate_schema(resp.json(), ERROR_SCHEMA)
    
    
@pytest.mark.auth
@pytest.mark.smoke
@pytest.mark.regression
def test_login_success(client: Any, validate_schema: Any) -> None:
    resp = client.post(
        "/login", json={"email": "eve.holt@reqres.in", "password": "cityslicka"}
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    validate_schema(body, LOGIN_SUCCESS_SCHEMA)
    assert body["token"]
    
    
@pytest.mark.auth
@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.parametrize(
    "payload",
    [{"email": "peter@klaven"}, {"password": "secret"}, {}],
    ids=["missing-password", "missing-email", "empty-body"],
)
def test_login_invalid_inputs(client: Any, validate_schema: Any, payload: dict) -> None:
    resp = client.post("/login", json=payload)
    assert resp.status_code == 400, resp.text
    validate_schema(resp.json(), ERROR_SCHEMA)