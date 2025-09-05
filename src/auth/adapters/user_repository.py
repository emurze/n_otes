from sqlalchemy import select, exists
from sqlalchemy.orm import load_only

from auth.models import User
from shared.repositories import SqlAlchemyGenericRepository


class UserSqlAlchemyRepository(SqlAlchemyGenericRepository[User]):
    async def get_by_username(
        self,
        username: str,
        load_fields: list | None = None,
    ) -> User | None:
        query = (
            select(self.model_class)
            .where(self.model_class.username == username)
            .options(
                load_only(*[getattr(User, field) for field in load_fields])
            )
        )
        res = await self._session.execute(query)
        return res.scalar_one_or_none()

    async def check_by_username(self, username: str) -> bool:
        query = select(exists().where(self.model_class.username == username))
        return (await self._session.execute(query)).scalar()

    async def check_by_email(self, email: str) -> bool:
        query = select(exists().where(self.model_class.email == email))
        return (await self._session.execute(query)).scalar()
