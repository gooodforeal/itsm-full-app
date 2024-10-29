from pydantic import BaseModel


class GetDialogSchema(BaseModel):
    sender_token: str
    recipient_username: str


class SendDialogSchema(GetDialogSchema):
    message: str
