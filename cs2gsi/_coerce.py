from __future__ import annotations

from collections.abc import Mapping
from enum import Enum
from typing import Any, TypeVar

from .models import Vector3

_EnumT = TypeVar("_EnumT", bound=Enum)

_TRUE_STRINGS = frozenset({"true", "1"})
_FALSE_STRINGS = frozenset({"false", "0"})


def as_mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def to_str(value: Any) -> str | None:
    if value is None:
        return None
    return value if isinstance(value, str) else str(value)


def to_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value) if value.is_integer() else None
    if isinstance(value, str):
        try:
            return int(value.strip())
        except ValueError:
            parsed = to_float(value)
            return int(parsed) if parsed is not None and parsed.is_integer() else None
    return None


def to_float(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.strip())
        except ValueError:
            return None
    return None


def to_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value != 0
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in _TRUE_STRINGS:
            return True
        if lowered in _FALSE_STRINGS:
            return False
    return None


def to_enum(enum_cls: type[_EnumT], value: Any) -> _EnumT | None:
    if value is None:
        return None
    try:
        return enum_cls(value)
    except ValueError:
        return None


def to_vector(value: Any) -> Vector3 | None:
    if isinstance(value, str):
        parts: list[Any] = value.split(",")
    elif isinstance(value, (list, tuple)):
        parts = list(value)
    else:
        return None
    if len(parts) != 3:
        return None
    coordinates = [to_float(part) for part in parts]
    if any(c is None for c in coordinates):
        return None
    x, y, z = coordinates
    return Vector3(x, y, z)
