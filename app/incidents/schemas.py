from enum import Enum

from pydantic import BaseModel, Field


class StatusEnum(Enum):
    opened = "Открыт"
    in_work = "В работе"
    closed = "Закрыт"


class ServiceLineEnum(Enum):
    build = "Сборка"
    repair = "Ремонт"
    administration = "Администрирование"


class GetAllIncidentsSchema(BaseModel):
    token: str


class GetAllIncidentsAdminSchema(BaseModel):
    token: str


class EditIncidentSchema(BaseModel):
    token: str
    incident_id: int
    incident_status_name: StatusEnum


class CreateIncidentSchema(BaseModel):
    token: str
    incident_name: str
    incident_description: str
    service_line_name: ServiceLineEnum


class CreateIncidentClientSchema(BaseModel):
    service_line_name: ServiceLineEnum
    client_fio: str
    incident_name: str
    incident_description: str

