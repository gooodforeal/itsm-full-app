from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, int_pk


class Dialogs(Base):
    __tablename__ = "dialogs"

    id: Mapped[int_pk]
    sender_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    recipient_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    message: Mapped[str]

    sender = relationship(
        "Users", foreign_keys=[sender_id],
        back_populates="sent_messages"
    )
    recipient = relationship(
        "Users", foreign_keys=[recipient_id],
        back_populates="received_messages"
    )

    extend_existing = True
