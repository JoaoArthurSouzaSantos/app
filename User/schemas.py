from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    perfil: int


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    perfil: int
