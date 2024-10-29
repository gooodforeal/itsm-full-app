from pydantic import BaseModel, Field


class SUserRegister(BaseModel):
    fio: str = Field(..., min_length=10, max_length=50, description="ФИО")
    username: str = Field(..., min_length=8, max_length=15, description="Имя пользователя")
    password: str = Field(..., min_length=8, max_length=15, description="Пароль, от 8 до 15 знаков")


class SUserAuth(BaseModel):
    username: str = Field(..., min_length=8, max_length=15, description="Имя пользователя")
    password: str = Field(..., min_length=8, max_length=15, description="Пароль, от 5 до 15 знаков")


class SUserToken(BaseModel):
    token: str