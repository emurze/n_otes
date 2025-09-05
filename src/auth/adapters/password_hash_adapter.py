import bcrypt


class PasswordHashAdapter:
    """A class responsible for hashing and verifying passwords using bcrypt."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hashes the provided password using bcrypt."""
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verifies if the provided password matches the hashed password."""
        hashed_password = hashed_password.encode("utf-8")
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
