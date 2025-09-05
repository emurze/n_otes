from dataclasses import dataclass


@dataclass(eq=False)
class ApplicationException(Exception):
    message: str = "Application error occurred"
