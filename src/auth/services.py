# async def authenticate_user_by_access_token() -> dict | NoReturn:
#     try:
#         payload = jwt_adapter.get_access_token_payload(command.access_token)
#     except TokenInvalidException as e:
#         raise UserNotAuthenticatedException(e.message)
#
#     async with uow:
#         user = await uow.users.get_by_id_with_group(UUID(payload.sub))
#
#         if user is None:
#             raise UserNotAuthenticatedException()
#
#         if command.required_roles and user.role not in command.required_roles:
#             raise UserNotAuthenticatedException("Insufficient privileges")
#
#         if command.return_tokens:
#             return map_user_to_tokens(jwt_adapter, user)
#         else:
#             return map_user_to_dto(user)
