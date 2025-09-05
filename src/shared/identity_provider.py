import uuid


def provide_identity() -> uuid.UUID:
    return uuid.uuid4()
