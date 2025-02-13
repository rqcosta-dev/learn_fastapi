from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict, EmailStr
from fast_zero.models import TodoState


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


class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState


class TodoSchemaPublic(TodoSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class TodoSchemaList(BaseModel):
    todos: list[TodoSchemaPublic]


class TodoSchemaUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None


class FilterPage(BaseModel):
    offset: int = 0
    limit: int = 100


class FilterTodo(FilterPage):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None
