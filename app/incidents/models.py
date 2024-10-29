from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, int_pk


class Statuses(Base):
    __tablename__ = "statuses"

    id: Mapped[int_pk]
    name: Mapped[str]

    incidents = relationship("Incidents", back_populates="status")

    extend_existing = True


class Incidents(Base):
    __tablename__ = "incidents"

    id: Mapped[int_pk]
    from_client_fio: Mapped[str] = mapped_column(nullable=True)
    name: Mapped[str]
    description: Mapped[str]

    status_id: Mapped[int] = mapped_column(
        ForeignKey("statuses.id", ondelete="CASCADE"),
        default=1
    )
    status = relationship("Statuses", back_populates="incidents")

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True
    )
    user = relationship("Users", back_populates="incidents")

    service_line_id: Mapped[int] = mapped_column(
        ForeignKey("service_lines.id", ondelete="CASCADE")
    )
    service_line = relationship("ServiceLines", back_populates="incidents")

    extend_existing = True
