from sqlalchemy import select, exists

from auth.models import User
from shared.repositories import SqlAlchemyGenericRepository


class UserSqlAlchemyRepository(SqlAlchemyGenericRepository[User]):
    async def get_by_username(self, username: str) -> User | None:
        query = select(self.model_class).where(
            self.model_class.username == username
        )
        res = await self._session.execute(query)
        return res.scalar_one_or_none()

    async def check_by_username(self, username: str) -> bool:
        query = select(exists().where(self.model_class.username == username))
        return (await self._session.execute(query)).scalar()

    async def check_by_email(self, email: str) -> bool:
        query = select(exists().where(self.model_class.email == email))
        return (await self._session.execute(query)).scalar()

    async def check_by_phone_number(self, phone_number: str) -> bool:
        query = select(
            exists().where(self.model_class.phone_number == phone_number)
        )
        return (await self._session.execute(query)).scalar()
