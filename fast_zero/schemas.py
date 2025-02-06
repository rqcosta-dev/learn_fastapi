from typing import List
from pydantic import BaseModel, EmailStr, ConfigDict


class MessageSchema(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserSchemaPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserSchemaList(BaseModel):
    users: List[UserSchemaPublic]


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
