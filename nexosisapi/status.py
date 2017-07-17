from enum import Enum


class Status(Enum):
    requested = 0,
    started = 1,
    completed = 2,
    cancelled = 3,
    failed = 4,
    estimated = 5
