from __future__ import annotations

from typing import Any, Mapping, Optional
import requests

class ApiClient:
    def __init__(self, base_url: str, api_key: str, timeout: int = 10) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update(
            {
                "x-api-key": api_key,
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )


def _url(self, path: str) -> str:
    if path.startswith(("http://", "https://")):
        return path
    return f"{self.base_url}/{path.lstrip('/')}"


def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
    kwargs.setdefault("timeout", self.timeout)
    return self._session.request(method, self._url(path), **kwargs)


def get(
    self, path: str, params: Optional[Mapping[str, Any]] = None, **kw: Any
) -> requests.Response:
    return self._request("GET", path, params=params, **kw)


def post(self, path: str, json: Optional[Any] = None, **kw: Any) -> requests.Response:
    return self._request("POST", path, json=json, **kw)


def put(self, path: str, json: Optional[Any] = None, **kw: Any) -> requests.Response:
    return self._request("PUT", path, json=json, **kw)


def patch(self, path: str, json: Optional[Any] = None, **kw: Any) -> requests.Response:
    return self._request("PATCH", path, json=json, **kw)


def delete(self, path: str, **kw: Any) -> requests.Response:
    return self._request("DELETE", path, **kw)


def close(self) -> None:
    self._session.close()
