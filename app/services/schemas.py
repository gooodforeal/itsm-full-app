from pydantic import BaseModel, Field


class EditServiceSchema(BaseModel):
    token: str
    service_id: int
    service_name: str
    service_description: str


class CreateServiceSchema(BaseModel):
    token: str
    service_type_name: str
    service_line_name: str
    service_name: str
    service_description: str


class DeleteServiceSchema(BaseModel):
    token: str
    service_id: int
