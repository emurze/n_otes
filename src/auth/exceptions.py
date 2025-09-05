from dataclasses import dataclass

from shared.exceptions import DomainException


@dataclass(eq=False)
class TokenInvalidException(DomainException):
    message: str = "Token is invalid."


@dataclass(eq=False)
class ApplicationException(Exception):
    message: str = "Application error occurred"


@dataclass(eq=False)
class UserConflictException(ApplicationException):
    pass


@dataclass(eq=False)
class UserNotAuthenticatedException(Exception):
    message: str = "User is not authenticated"


@dataclass(eq=False)
class UserNotFoundException(Exception):
    message: str = "User not found"
