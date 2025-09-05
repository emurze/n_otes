from dataclasses import dataclass

from shared.exceptions import ApplicationException


@dataclass(eq=False)
class NoteNotFoundException(ApplicationException):
    message: str = "Note not found"
