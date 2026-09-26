"""ReqRes /unknown resource contract tests (list + not-found)."""

from __future__ import annotations

from typing import Any

import pytest

from schemas import RESOURCE_LIST_SCHEMA


@pytest.mark.resources
@pytest.mark.smoke
@pytest.mark.regression
def test_list_resources(client: Any, validate_schema: Any) -> None:
    resp = client.get("/unknown")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    validate_schema(body, RESOURCE_LIST_SCHEMA)
    assert body["data"], "resource list should not be empty"
    for item in body["data"]:
        assert isinstance(item["id"], int)
        assert item["name"]


@pytest.mark.resources
@pytest.mark.regression
@pytest.mark.negative
def test_missing_resource_returns_404(client: Any) -> None:
    resp = client.get("/unknown/23")
    assert resp.status_code == 404, resp.text
    assert resp.json() == {}
