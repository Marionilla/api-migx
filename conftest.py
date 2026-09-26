from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Iterator

import pytest
from jsonschema import Draft7Validator, FormatChecker

#Make utils/ and schemas/ importable regardless of where pytest is run from.
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
    
from utils import ApiClient # noqa: E402

#Load a local .env if present (optional).
try:
    from dotenv import load_dotenv

    load_dotenv(ROOT / ".env")
except ImportError:
    pass

DEFAULT_BASE_URL = "https://reqres.in/api"
DEFAULT_API_KEY = "reqres-free-v1"

@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("REQRES_BASE_URL", DEFAULT_BASE_URL).rstrip("/")

@pytest.fixture(scope="session")
def api_key() -> str:
    return os.getenv("REQRES_API_KEY", DEFAULT_API_KEY)

@pytest.fixture(scope="session")
def client(base_url: str, api_key: str) -> Iterator[ApiClient]:
    api = ApiClient(base_url=base_url, api_key=api_key, timeout=10)
    yield api
    api.close()
    
@pytest.fixture(scope="session")
def validate_schema() -> Any:
    def _validate(instance: Any, schema: dict) -> None:
        validator = Draft7Validator(schema, format_checker=FormatChecker())
        errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
        if errors:
            details = "\n".join(
                f" - at {'/'.join(map(str, err.path)) or '<root>'}: {err.message}"
                for err in errors
            )
            raise AssertionError(f"Schema validation failed:\n{details}")

    return _validate