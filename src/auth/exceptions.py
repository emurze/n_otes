from dataclasses import dataclass

from shared.exceptions import ApplicationException


@dataclass(eq=False)
class TokenInvalidException(ApplicationException):
    message: str = "Token is invalid."


@dataclass(eq=False)
class UserConflictException(ApplicationException):
    pass


@dataclass(eq=False)
class UserNotAuthenticatedException(ApplicationException):
    message: str = "User is not authenticated"


@dataclass(eq=False)
class UserNotFoundException(ApplicationException):
    message: str = "User not found"
