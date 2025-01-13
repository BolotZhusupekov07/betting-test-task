from enum import StrEnum


class EventStateEnum(StrEnum):
    NEW = 'NEW'
    FINISHED_WIN = 'FINISHED_WIN'
    FINISHED_LOSE = 'FINISHED_LOSE'


class EventStateUpdateInEnum(StrEnum):
    FINISHED_WIN = 'FINISHED_WIN'
    FINISHED_LOSE = 'FINISHED_LOSE'
