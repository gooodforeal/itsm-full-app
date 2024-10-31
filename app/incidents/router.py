from fastapi import APIRouter

from app.incidents.dao import IncidentsDAO, StatusesDAO
from app.services.dao import ServiceLinesDAO
from app.incidents.schemas import GetAllIncidentsAdminSchema, GetAllIncidentsSchema, EditIncidentSchema, CreateIncidentSchema, CreateIncidentClientSchema
from app.users.dependencies import get_current_user, is_admin_user, is_tech_user


router = APIRouter(prefix='/incidents', tags=['incidents'])


@router.get("/incident/{incident_id}")
async def get_incident(incident_id: int):
    incident = await IncidentsDAO.find_one_or_none_joined_by_id(incident_id=incident_id)
    return {
        "status": "ok",
        "message": "Successful request!",
        "data": incident
    }


@router.get("/statuses/all")
async def get_all_incidents():
    statuses = await IncidentsDAO.find_all_statuses()
    return {
        "status": "ok",
        "message": "Successful request!",
        "data": statuses
    }


@router.post("/all")
async def get_all_incidents(user: GetAllIncidentsSchema):
    current_user = await get_current_user(user.token)
    user_id = current_user.id
    incidents = await IncidentsDAO.find_all_joined_by_user_id(user_id=user_id)
    return {
        "status": "ok",
        "message": "Successful request!",
        "data": incidents
    }


@router.post("/create")
async def create_incident(incident: CreateIncidentSchema):
    current_user = await get_current_user(incident.token)
    service_line = await ServiceLinesDAO.find_one_or_none(name=incident.service_line_name.value)
    incident_dict = incident.dict()
    incident_dict["user_id"] = current_user.id
    incident_dict["service_line_id"] = service_line.id
    new_incident = await IncidentsDAO.create_incident(data=incident_dict)
    return {
        "status": "ok",
        "message": "Successful request!",
        "data": new_incident
    }


@router.post("/client/create")
async def create_client_incident(incident: CreateIncidentClientSchema):
    service_line = await ServiceLinesDAO.find_one_or_none(name=incident.service_line_name.value)
    incident_dict = incident.dict()
    incident_dict["service_line_id"] = service_line.id
    new_incident = await IncidentsDAO.create_client_incident(data=incident_dict)
    return {
        "status": "ok",
        "message": "Successful request!",
        "data": new_incident
    }


@router.post("/edit")
async def edit_incident(incident: EditIncidentSchema):
    current_user = await get_current_user(incident.token)
    current_user_id = current_user.id
    if await is_admin_user(incident.token):
        incident_dict = incident.dict()
        incident_status = await StatusesDAO.find_one_or_none(name=incident.incident_status_name.value)
        incident_dict["incident_status_name"] = incident_status.id
        incident_dict["incident_solver_id"] = current_user_id
        edited_incident = await IncidentsDAO.edit_incident(incident_dict)
        return {
            "status": "ok",
            "message": "Successful request!",
            "data": edited_incident
        }
    else:
        return {
            "status": "Error",
            "message": "Not enough rights!",
            "data": None
        }


@router.post("/admin/all")
async def get_all_incidents(user: GetAllIncidentsAdminSchema):
    if (await is_admin_user(user.token)) or await is_tech_user(user.token):
        incidents = await IncidentsDAO.find_all_joined()
        return {
            "status": "ok",
            "message": "Successful request!",
            "data": incidents
        }
    else:
        return {
            "status": "Error",
            "message": "Not enough rights!",
            "data": None
        }
