from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Union
from uuid import UUID

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from auth.exceptions import TokenInvalidException
from shared.identity_provider import provide_identity


@dataclass(frozen=True)
class RefreshTokenPayloadDTO:
    sub: str
    type: str
    iat: int
    exp: int
    jti: str


@dataclass(frozen=True)
class AccessTokenPayloadDTO:
    sub: str
    username: str
    email: str
    type: str
    iat: int
    exp: int
    jti: str


@dataclass(slots=True, frozen=True)
class JWTAdapter:
    secret: str
    algorithm: str
    token_type_key: str
    access_token_type: str
    refresh_token_type: str
    refresh_token_expire_days: int
    access_token_expire_minutes: int

    def _encode_jwt(
        self,
        token_type: str,
        token_data: dict,
        expire_timedelta: timedelta,
    ) -> str:
        now = datetime.now(UTC)
        payload = {
            **token_data,
            self.token_type_key: token_type,
            "iat": now,
            "exp": now + expire_timedelta,
            "jti": str(provide_identity()),
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def _decode_jwt(self, jwt_token: str, required_token_type: str) -> dict:
        try:
            payload = jwt.decode(
                jwt_token,
                self.secret,
                algorithms=[self.algorithm],
            )
        except ExpiredSignatureError:
            raise TokenInvalidException("Token is expired")

        except InvalidTokenError:
            raise TokenInvalidException("Token is invalid")

        if payload.get(self.token_type_key) != required_token_type:
            raise TokenInvalidException("Token type is invalid")

        return payload

    def create_access_token(
        self,
        user_id: UUID,
        username: str,
        email: str,
        expire_minutes: Union[int, None] = None,
    ) -> str:
        payload = {
            "sub": str(user_id),
            "username": username,
            "email": email,
        }
        return self._encode_jwt(
            token_type=self.access_token_type,
            token_data=payload,
            expire_timedelta=timedelta(
                minutes=expire_minutes or self.access_token_expire_minutes,
            ),
        )

    def create_refresh_token(
        self,
        user_id: UUID,
        expire_days: Union[int, None] = None,
    ) -> str:
        payload = {
            "sub": str(user_id),
        }
        return self._encode_jwt(
            token_type=self.refresh_token_type,
            token_data=payload,
            expire_timedelta=timedelta(
                days=expire_days or self.refresh_token_expire_days,
            ),
        )

    def get_refresh_token_payload(
        self,
        refresh_token: str,
    ) -> RefreshTokenPayloadDTO:
        token_data = self._decode_jwt(refresh_token, self.refresh_token_type)
        return RefreshTokenPayloadDTO(**token_data)

    def get_access_token_payload(
        self,
        access_token: str,
    ) -> AccessTokenPayloadDTO:
        token_data = self._decode_jwt(access_token, self.access_token_type)
        return AccessTokenPayloadDTO(**token_data)
