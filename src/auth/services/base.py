from auth.adapters.jwt_adapter import JWTAdapter
from auth.models import User


def map_user_to_dto(user: User) -> dict:
    return {
        "id": user.id,
        "name": user.name,
        "surname": user.surname,
        "username": user.username,
        "phone_number": user.phone_number if user.phone_number else None,
        "email": user.email,
    }


def map_user_to_tokens(jwt_adapter: JWTAdapter, user: User) -> dict:
    return {
        "access_token": jwt_adapter.create_access_token(
            user_id=user.id,
            username=user.username,
            email=user.email,
        ),
        "refresh_token": jwt_adapter.create_refresh_token(user_id=user.id),
    }
