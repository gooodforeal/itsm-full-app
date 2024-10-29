from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload, load_only

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.incidents.models import Incidents, Statuses
from app.services.models import ServiceLines
from app.users.models import Users


class IncidentsDAO(BaseDAO):
    model = Incidents

    @classmethod
    async def find_one_or_none_joined_by_id(cls, incident_id: int):
        async with async_session_maker() as session:
            query = (
                select(Incidents)
                .options(load_only(Incidents.id, Incidents.created_at, Incidents.from_client_fio, Incidents.name, Incidents.description))
                .options(joinedload(Incidents.status).load_only(Statuses.name))
                .options(joinedload(Incidents.service_line).load_only(ServiceLines.name))
                .options(joinedload(Incidents.user).load_only(Users.username, Users.fio))
                .filter_by(id=incident_id)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all_joined(cls):
        async with async_session_maker() as session:
            query = (
                select(Incidents)
                .options(joinedload(Incidents.status))
                .options(joinedload(Incidents.service_line).load_only(ServiceLines.name))
                .options(joinedload(Incidents.user).load_only(Users.username, Users.fio))
            )
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_all_statuses(cls):
        async with async_session_maker() as session:
            query = (
                select(Statuses)
            )
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_all_joined_by_user_id(cls, user_id):
        async with async_session_maker() as session:
            query = (
                select(Incidents)
                .options(load_only(Incidents.from_client_fio, Incidents.name, Incidents.created_at))
                .options(joinedload(Incidents.status))
                .options(joinedload(Incidents.service_line).load_only(ServiceLines.name))
                .options(joinedload(Incidents.user).load_only(Users.username, Users.fio))
                .filter(Incidents.user_id == user_id)
            )
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def edit_incident(cls, data: dict):
        async with async_session_maker() as session:
            stmt = (
                update(Incidents)
                .where(Incidents.id == data["incident_id"])
                .values(status_id=data["incident_status_name"])
            )
            res = await session.execute(stmt)
            await session.commit()
            return res

    @classmethod
    async def create_incident(cls, data: dict):
        async with async_session_maker() as session:
            get_user = (
                select(Users)
                .filter_by(id=data["user_id"])
            )
            user_orm = (await session.execute(get_user)).scalar_one()

            get_service_line = (
                select(ServiceLines)
                .filter_by(id=data["service_line_id"])
            )
            service_line_orm = (await session.execute(get_service_line)).scalar_one()

            new_incident = Incidents(
                user_id=data["user_id"],
                service_line_id=data["service_line_id"],
                name=data["incident_name"],
                description=data["incident_description"],
                user=user_orm,
                service_line=service_line_orm
            )
            session.add(new_incident)

            try:
                await session.commit()
                return new_incident
            except SQLAlchemyError as e:
                await session.rollback()
                raise e

    @classmethod
    async def create_client_incident(cls, data: dict):
        async with async_session_maker() as session:
            get_service_line = (
                select(ServiceLines)
                .filter_by(id=data["service_line_id"])
            )
            service_line_orm = (await session.execute(get_service_line)).scalar_one()

            new_incident = Incidents(
                from_client_fio=data["client_fio"],
                service_line_id=data["service_line_id"],
                name=data["incident_name"],
                description=data["incident_description"],
                service_line=service_line_orm
            )
            session.add(new_incident)

            try:
                await session.commit()
                return new_incident
            except SQLAlchemyError as e:
                await session.rollback()
                raise e


class StatusesDAO(BaseDAO):
    model = Statuses