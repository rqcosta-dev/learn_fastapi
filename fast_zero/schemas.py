from typing import List
from pydantic import BaseModel, EmailStr


class MessageSchema(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDB(UserSchema):
    id: int


class UserSchemaPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserSchemaList(BaseModel):
    users: List[UserSchemaPublic]
