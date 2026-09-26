from __future__ import annotations
from typing import Any, Dict

DRAFT_07 = "http://json-schema.org/draft-07/schema#"

# --- building blocks ---
USER_OBJECT_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "required": ["id", "email", "first_name", "last_name", "avatar"],
    "properties": {
        "id": {"type": "integer", "minimum": 1},
        "email": {"type": "string", "format": "email"},
        "first_name": {"type": "string", "minLength": 1},
        "last_name": {"type": "string", "minLength": 1},
        "avatar": {"type": "string", "format": "uri"},
    },
    "additionalProperties": False,
}

RESOURCE_OBJECT_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "required": ["id", "name", "year", "color", "pantone_value"],
    "properties": {
        "id": {"type": "integer", "minimum": 1},
        "name": {"type": "string", "minLength": 1},
        "year": {"type": "integer"},
        "color": {"type": "string"},
        "pantone_value": {"type": "string"},
    },
    "additionalProperties": False,
}

_SUPPORT: Dict[str, Any] = {"type": "object"}

#--- paginated lists - --
USER_LIST_SCHEMA: Dict[str, Any] = {
    "$schema": DRAFT_07,
    "type": "object",
    "required": ["page", "per_page", "total", "total_pages", "data"],
    "properties": {
        "page": {"type": "integer", "minimum": 1},
        "per_page": {"type": "integer", "minimum": 1},
        "total": {"type": "integer", "minimum": 0},
        "total_pages": {"type": "integer", "minimum": 0},
        "data": {"type": "array", "items": USER_OBJECT_SCHEMA},
        "support": _SUPPORT,
    },
    "additionalProperties": True,
}

RESOURCE_LIST_SCHEMA: Dict[str, Any] = {
    "$schema": DRAFT_07,
    "type": "object",
    "required": ["page", "per_page", "total", "total_pages", "data"],
    "properties": {
        "page": {"type": "integer"},
        "per_page": {"type": "integer"},
        "total": {"type": "integer"},
        "total_pages": {"type": "integer"},
        "data": {"type": "array", "items": RESOURCE_OBJECT_SCHEMA},
        "support": _SUPPORT,
    },
    "additionalProperties": True,
}

#--- single item - --
SINGLE_USER_SCHEMA: Dict[str, Any] = {
    "$schema": DRAFT_07,
    "type": "object",
    "required": ["data"],
    "properties": {"data": USER_OBJECT_SCHEMA, "support": _SUPPORT},
    "additionalProperties": True,
}

#--- writes - --
CREATE_USER_SCHEMA: Dict[str, Any] = {
    "$schema": DRAFT_07,
    "type": "object",
    "required": ["name", "job", "id", "createdAt"],
    "properties": {
        "name": {"type": "string"},
        "job": {"type": "string"},
        "id": {"type": "string"},
        "createdAt": {"type": "string", "format": "date-time"},
    },
    "additionalProperties": True,
}

UPDATE_USER_SCHEMA: Dict[str, Any] = {
    "$schema": DRAFT_07,
    "type": "object",
    "required": ["updatedAt"],
    "properties": {
        "name": {"type": "string"},
        "job": {"type": "string"},
        "updatedAt": {"type": "string", "format": "date-time"},
    },
    "additionalProperties": True,
}

#--- auth(allow ReqRes's _meta block) ---
REGISTER_SUCCESS_SCHEMA: Dict[str, Any] = {
    "$schema": DRAFT_07,
    "type": "object",
    "required": ["id", "token"],
    "properties": {
        "id": {"type": "integer"},
        "token": {"type": "string", "minLength": 1},
        "_meta": {"type": "object"},
    },
    "additionalProperties": False,
}

LOGIN_SUCCESS_SCHEMA: Dict[str, Any] = {
    "$schema": DRAFT_07,
    "type": "object",
    "required": ["token"],
    "properties": {
        "token": {"type": "string", "minLength": 1},
        "_meta": {"type": "object"},
    },
    "additionalProperties": False,
}

ERROR_SCHEMA: Dict[str, Any] = {
    "$schema": DRAFT_07,
    "type": "object",
    "required": ["error"],
    "properties": {"error": {"type": "string", "minLength": 1}, "_meta": {"type": "object"}},
    "additionalProperties": False,
}