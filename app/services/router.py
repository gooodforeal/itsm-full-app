from fastapi import APIRouter

from app.services.dao import ServicesDAO, ServiceLinesDAO, ServiceTypesDAO
from app.services.schemas import EditServiceSchema, CreateServiceSchema, DeleteServiceSchema
from app.users.dependencies import is_admin_user, get_current_user


router = APIRouter(prefix='/services', tags=['services'])


@router.get("/lines/all")
async def get_all_service_lines():
    lines = await ServiceLinesDAO.find_all()
    return {
        "status": "ok",
        "message": "Successful request!",
        "data": lines
    }


@router.get("/service/{service_id}")
async def get_service(service_id: int):
    service = await ServicesDAO.find_one_or_none_joined_by_id(service_id=service_id)
    return {
        "status": "ok",
        "message": "Successful request!",
        "data": service
    }


@router.post("/create")
async def edit_service(service: CreateServiceSchema):
    service_type = await ServiceTypesDAO.find_one_or_none(name=service.service_type_name)
    service_line = await ServiceLinesDAO.find_one_or_none(name=service.service_line_name)

    service_dict = service.dict()
    service_dict["service_type_name"] = service_type.id
    service_dict["service_line_name"] = service_line.id

    new_service = await ServicesDAO.create_service(data=service_dict)

    return {
        "status": "ok",
        "message": "Successful creation!",
        "data": new_service
    }


@router.post("/delete/")
async def delete_service_by_id(service: DeleteServiceSchema):
    await get_current_user(service.token)
    check = await ServicesDAO.delete(id=service.service_id)
    if check:
        return {
            "status": "ok",
            "message": "Successful delete!",
            "data": None
        }
    else:
        return {
            "status": "Error",
            "message": "Can't delete!",
            "data": None
        }


@router.post("/edit")
async def edit_service(service: EditServiceSchema):
    await get_current_user(service.token)
    edited_service = await ServicesDAO.edit_service(
        service_id=service.service_id,
        service_name=service.service_name,
        service_description=service.service_description
    )
    return {
        "status": "ok",
        "message": "Successful edit!",
        "data": edited_service
    }


@router.get("/all")
async def get_all_services():
    services = await ServicesDAO.find_all_joined()
    return {
        "status": "ok",
        "message": "Successful request!",
        "data": services
    }
