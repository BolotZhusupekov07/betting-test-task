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


class EventAPIException(CommonException):
    default_message = (
        "Something went wrong, we are trying everything to get it back on"
    )
    error_code = "EventAPIError"
