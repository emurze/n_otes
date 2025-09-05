from fastapi import APIRouter, Depends, Form, HTTPException
from starlette import status

from auth import services
from auth.adapters.jwt_adapter import JWTAdapter
from auth.adapters.password_hash_adapter import PasswordHashAdapter
from auth.dependencies import get_refresh_token
from auth.exceptions import UserNotAuthenticatedException, UserConflictException
from auth.schemas import TokenRead, UserSignup
from auth.services import register_user
from auth.services.authenticate_by_credentials import authenticate_user_by_credentials
from shared.dependencies import get_uow, get_ph, get_jwt_adapter
from shared.schemas import ErrorSchema
from shared.uows import SqlAlchemyUnitOfWork

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=TokenRead,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
        status.HTTP_409_CONFLICT: {"model": ErrorSchema},
    },
)
async def sign_up(
    user_dto: UserSignup,
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
    ph: PasswordHashAdapter = Depends(get_ph),
    jwt_adapter: JWTAdapter = Depends(get_jwt_adapter),
):
    try:
        await register_user(
            uow=uow,
            ph=ph,
            name=user_dto.name,
            username=user_dto.username,
            surname=user_dto.surname,
            password=user_dto.password,
            email=user_dto.email,
        )

    except UserConflictException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )

    return await authenticate_user_by_credentials(
        uow=uow,
        ph=ph,
        jwt_adapter=jwt_adapter,
        username=user_dto.username,
        password=user_dto.password,
    )


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=TokenRead,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorSchema},
    },
)
async def login(
    username: str = Form(),
    password: str = Form(),
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
    ph: PasswordHashAdapter = Depends(get_ph),
    jwt_adapter: JWTAdapter = Depends(get_jwt_adapter),
):
    try:
        return await authenticate_user_by_credentials(
            uow=uow,
            ph=ph,
            jwt_adapter=jwt_adapter,
            username=username,
            password=password,
        )

    except UserNotAuthenticatedException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
        )


@router.post(
    "/refresh-token",
    status_code=status.HTTP_200_OK,
    response_model=TokenRead,
    response_model_exclude_none=True,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorSchema},
    },
)
async def refresh_tokens(
    refresh_token: str = Depends(get_refresh_token),
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
    jwt_adapter: JWTAdapter = Depends(get_jwt_adapter),
):
    try:
        return await services.refresh_tokens(
            uow=uow,
            jwt_adapter=jwt_adapter,
            refresh_token=refresh_token,
        )

    except UserNotAuthenticatedException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
        )
