from src.common.exceptions import (
    CommonException,
    ObjectAlreadyExistsException,
    ObjectNotFoundException,
)


class EventAlreadyExistsException(ObjectAlreadyExistsException):
    default_message = "Event already exists"
    error_code = "EventAlreadyExistsError"


class EventNotFoundException(ObjectNotFoundException):
    default_message = "Event Not Found"
    error_code = "EventNotFound"


class EventInvalidException(CommonException):
    default_message = "Event is invalid"
    error_code = "EventInvalidError"
