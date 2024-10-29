from fastapi import APIRouter

from app.dialogs.schemas import GetDialogSchema, SendDialogSchema
from app.users.dependencies import get_current_user
from app.users.dao import UsersDAO
from app.dialogs.dao import DialogsDAO


router = APIRouter(prefix='/dialogs', tags=['dialogs'])


@router.post("/dialog")
async def get_dialog(dialog: GetDialogSchema):
    sender_user = await get_current_user(dialog.sender_token)
    recipient = await UsersDAO.find_one_or_none(username=dialog.recipient_username)

    if sender_user is None or recipient is None:
        return {
            "status": "Error",
            "message": "No such user!",
            "data": None
        }

    dialog_dict = dialog.dict()
    dialog_dict["sender_id"] = sender_user.id
    dialog_dict["recipient_id"] = recipient.id

    dialog_response = await DialogsDAO.find_dialog_joined(data=dialog_dict)

    return {
        "status": "ok",
        "message": "Successful request!",
        "data": dialog_response
    }


@router.post("/send_message")
async def get_dialog(dialog: SendDialogSchema):
    sender_user = await get_current_user(dialog.sender_token)
    recipient = await UsersDAO.find_one_or_none(username=dialog.recipient_username)

    if sender_user is None or recipient is None:
        return {
            "status": "Error",
            "message": "No such user!",
            "data": None
        }

    dialog_dict = dialog.dict()
    dialog_dict["sender_id"] = sender_user.id
    dialog_dict["recipient_id"] = recipient.id

    dialog_response = await DialogsDAO.send_message(data=dialog_dict)

    return {
        "status": "ok",
        "message": "Successful request!",
        "data": dialog_response
    }
