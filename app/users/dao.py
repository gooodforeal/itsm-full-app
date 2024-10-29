from sqlalchemy import select

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.users.models import Users


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def find_all_except_me(cls, my_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter(cls.model.id != my_id)
            result = await session.execute(query)
            return result.scalars().all()
