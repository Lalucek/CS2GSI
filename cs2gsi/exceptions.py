"""Exception hierarchy of the :mod:`cs2gsi` package."""

from __future__ import annotations

__all__ = ["CS2GSIError", "PayloadError"]


class CS2GSIError(Exception):
    """Base class for all errors raised by :mod:`cs2gsi`."""


class PayloadError(CS2GSIError, ValueError):
    """Raised when a GSI payload has an invalid structure."""
