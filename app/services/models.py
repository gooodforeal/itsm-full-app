from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, int_pk


class ServiceLines(Base):
    __tablename__ = "service_lines"

    id: Mapped[int_pk]
    name: Mapped[str]

    services = relationship("Services", back_populates="service_line")
    incidents = relationship("Incidents", back_populates="service_line")

    extend_existing = True


class ServiceTypes(Base):
    __tablename__ = "service_types"

    id: Mapped[int_pk]
    name: Mapped[str]

    services = relationship("Services", back_populates="service_type")

    extend_existing = True


class Services(Base):
    __tablename__ = "services"

    id: Mapped[int_pk]
    name: Mapped[str]
    description: Mapped[str]

    service_type_id: Mapped[int] = mapped_column(
        ForeignKey("service_types.id", ondelete="CASCADE")
    )
    service_type = relationship("ServiceTypes", back_populates="services")

    service_line_id: Mapped[int] = mapped_column(
        ForeignKey("service_lines.id", ondelete="CASCADE")
    )
    service_line = relationship("ServiceLines", back_populates="services")

    extend_existing = True


