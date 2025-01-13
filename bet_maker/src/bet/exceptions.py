from src.common.exceptions import (
    ObjectAlreadyExistsException,
    ObjectNotFoundException,
)


class BetAlreadyExistsException(ObjectAlreadyExistsException):
    default_message = "Bet already exists"
    error_code = "BetAlreadyExistsError"


class BetNotFoundException(ObjectNotFoundException):
    default_message = "Bet Not Found"
    error_code = "BetNotFound"
