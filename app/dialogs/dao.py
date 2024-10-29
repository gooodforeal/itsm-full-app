from sqlalchemy import select, update, or_, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload, load_only

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.dialogs.models import Dialogs
from app.services.models import ServiceLines
from app.users.models import Users


class DialogsDAO(BaseDAO):
    model = Dialogs

    @classmethod
    async def find_dialog_joined(cls, data: dict):
        async with async_session_maker() as session:
            query = (
                select(Dialogs)
                .options(load_only(Dialogs.message, Dialogs.created_at))
                .options(joinedload(Dialogs.sender))
                .options(joinedload(Dialogs.recipient))
                .filter(
                    or_(
                        and_(
                            Dialogs.sender_id == data["sender_id"],
                            Dialogs.recipient_id == data["recipient_id"]
                        ),
                        and_(
                            Dialogs.sender_id == data["recipient_id"],
                            Dialogs.recipient_id == data["sender_id"]
                        )
                    )
                )
            )
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def send_message(cls, data: dict):
        async with async_session_maker() as session:
            get_sender = (
                select(Users)
                .filter_by(id=data["sender_id"])
            )
            sender_orm = (await session.execute(get_sender)).scalar_one()

            get_recipient = (
                select(Users)
                .filter_by(id=data["recipient_id"])
            )
            recipient_orm = (await session.execute(get_recipient)).scalar_one()

            new_dialog = Dialogs(
                sender_id=data["sender_id"],
                recipient_id=data["recipient_id"],
                sender=sender_orm,
                recipient=recipient_orm,
                message=data["message"]
            )
            session.add(new_dialog)
            try:
                await session.commit()
                return new_dialog
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
