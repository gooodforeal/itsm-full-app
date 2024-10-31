from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload, selectinload

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.services.models import Services, ServiceTypes, ServiceLines


class ServicesDAO(BaseDAO):
    model = Services

    @classmethod
    async def find_all_joined(cls):
        async with async_session_maker() as session:
            print(123)
            query = (
                select(Services)
                .options(joinedload(Services.service_type))
                .options(joinedload(Services.service_line))
                .order_by(Services.service_type_id)
                .order_by(Services.service_line_id)
            )
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none_joined_by_id(cls, service_id: int):
        async with async_session_maker() as session:
            query = (
                select(Services)
                .options(joinedload(Services.service_type))
                .options(joinedload(Services.service_line))
                .filter_by(id=service_id)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all_services_by_service_line(cls, service_line: str):
        async with async_session_maker() as session:
            query = (
                select(ServiceLines)
                .options(selectinload(ServiceLines.services).load_only(Services.description))
                .filter_by(name=service_line)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def create_service(cls, data: dict):
        async with async_session_maker() as session:
            get_new_service_line = (
                select(ServiceLines)
                .filter_by(id=data["service_line_name"])
            )
            service_line_orm = (await session.execute(get_new_service_line)).scalar_one()

            get_new_service_type = (
                select(ServiceTypes)
                .filter_by(id=data["service_type_name"])
            )
            service_type_orm = (await session.execute(get_new_service_type)).scalar_one()

            new_service = Services(
                service_line_id=data["service_line_name"],
                service_line=service_line_orm,
                service_type_id=data["service_type_name"],
                service_type=service_type_orm,
                name=data["service_name"],
                description=data["service_description"]
            )
            session.add(new_service)

            try:
                await session.commit()
                return new_service
            except SQLAlchemyError as e:
                await session.rollback()
                raise e

    @classmethod
    async def edit_service(cls, service_id: int, service_name: str, service_description: str):
        async with async_session_maker() as session:
            stmt = (
                update(Services)
                .where(Services.id == service_id)
                .values(name=service_name, description=service_description)
            )
            res = await session.execute(stmt)
            await session.commit()
            return res


class ServiceTypesDAO(BaseDAO):
    model = ServiceTypes


class ServiceLinesDAO(BaseDAO):
    model = ServiceLines
