from fastapi import Depends, HTTPException
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)
from starlette import status

from auth.adapters.jwt_adapter import JWTAdapter
from auth.exceptions import UserNotAuthenticatedException
from auth.schemas import UserRead
from auth.services import authenticate_user_by_access_token
from shared.dependencies import get_jwt_adapter, get_uow
from shared.uows import SqlAlchemyUnitOfWork

refresh_bearer = HTTPBearer(
    auto_error=False,
    scheme_name="RefreshTokenBearer",
)
access_bearer = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    scheme_name="AccessTokenBearer",
)


async def get_refresh_token(
    refresh_token: HTTPAuthorizationCredentials = Depends(refresh_bearer),
):
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return refresh_token.credentials


# async def get_owner(  # TODO:
#     uow: SqlAlchemyUnitOfWork = Depends(get_uow),
#     jwt_adapter: JWTAdapter = Depends(get_jwt_adapter),
#     access_token: str = Depends(access_bearer),
# ) -> UserRead:
#     try:
#         user_dict = await authenticate_user_by_access_token(
#             uow=uow,
#             jwt_adapter=jwt_adapter,
#             access_token=access_token,
#             return_tokens=False,
#         )
#         return UserRead.model_validate(user_dict)
#     except UserNotAuthenticatedException as e:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail=e.message,
#         )
