from typing import Annotated

from fastapi import APIRouter, Depends

from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dao import UsersDAO
from app.users.schemas import SUserRegister, SUserAuth, SUserToken
from app.users.dependencies import is_admin_user, is_tech_user

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post("/register/")
async def register_user(user_data: Annotated[SUserRegister, Depends()]) -> dict:
    user = await UsersDAO.find_one_or_none(username=user_data.username)
    if user:
        return {"status": "error", "message": "User already exists!"}
    user_dict = user_data.dict()
    user_dict['password'] = get_password_hash(user_data.password)
    await UsersDAO.add(**user_dict)
    return {"status": "ok", "message": "Successful registration!"}


@router.post("/login/")
async def auth_user(user_data: Annotated[SUserAuth, Depends()]):
    check = await authenticate_user(username=user_data.username, password=user_data.password)
    if check is None:
        return {"status": "error", "message": "Wrong username or password!"}
    access_token = create_access_token({"sub": str(check.id)})
    return {"status": "ok", "message": "Successful registration!", "token": access_token}


@router.post("/is_admin/")
async def is_admin(user: Annotated[SUserToken, Depends()]):
    if await is_admin_user(user.token):
        return {
            "status": "ok",
            "message": "Admin user!",
            "data": True
        }
    else:
        return {
            "status": "ok",
            "message": "Not admin user!",
            "data": False
        }


@router.post("/is_tech/")
async def is_tech(user: Annotated[SUserToken, Depends()]):
    if await is_tech_user(user.token):
        return {
            "status": "ok",
            "message": "Tech user!",
            "data": True
        }
    else:
        return {
            "status": "ok",
            "message": "Not tech user!",
            "data": False
        }


@router.get("/all")
async def all_users():
    users = await UsersDAO.find_all()
    return {
        "status": "ok",
        "message": "Successful request!!",
        "data": users
    }
