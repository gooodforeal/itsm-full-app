from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, str_uniq, int_pk
from app.dialogs.models import Dialogs
from app.incidents.models import Incidents


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    fio: Mapped[str]
    username: Mapped[str_uniq]
    password: Mapped[str]

    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_tech: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)

    incidents = relationship(
        "Incidents",
        foreign_keys=[Incidents.user_id],
        back_populates="user",
        cascade="all, delete",
    )
    solved_incidents = relationship(
        "Incidents",
        foreign_keys=[Incidents.solver_id],
        back_populates="solver",
        cascade="all, delete",
    )

    sent_messages = relationship(
        "Dialogs",
        foreign_keys=[Dialogs.sender_id],
        back_populates="sender",
        cascade="all, delete",
    )
    received_messages = relationship(
        "Dialogs",
        foreign_keys=[Dialogs.recipient_id],
        back_populates="recipient",
        cascade="all, delete",
    )

    extend_existing = True
