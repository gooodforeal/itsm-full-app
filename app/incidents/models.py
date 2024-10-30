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
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True
    )
    solver_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True
    )
    service_line_id: Mapped[int] = mapped_column(
        ForeignKey("service_lines.id", ondelete="CASCADE")
    )

    status = relationship("Statuses", back_populates="incidents")
    user = relationship("Users", back_populates="incidents", foreign_keys=[user_id])
    solver = relationship("Users", back_populates="solved_incidents", foreign_keys=[solver_id])
    service_line = relationship("ServiceLines", back_populates="incidents")

    extend_existing = True
