from enum import StrEnum


class BetStatusEnum(StrEnum):
    NEW = "NEW"
    WON = "WON"
    LOST = "LOST"


class BetStatusUpdateEnum(StrEnum):
    WON = "WON"
    LOST = "LOST"
