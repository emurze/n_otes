from dataclasses import dataclass

from shared.exceptions import DomainException


@dataclass(eq=False)
class TokenInvalidException(DomainException):
    message: str = "Token is invalid."
