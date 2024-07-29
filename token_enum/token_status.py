from enum import Enum


class Status(Enum):
    ALLOWED = "allowed"
    INVALID = "invalid"
    UNKNOWN = "unknown"
    NOT_ALLOWED = "not_allowed"
