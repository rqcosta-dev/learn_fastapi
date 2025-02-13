from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import Todo, User
from fast_zero.schemas import (
    FilterTodo,
    MessageSchema,
    TodoSchemaList,
    TodoSchema,
    TodoSchemaPublic,
    TodoSchemaUpdate,
)
from fast_zero.security import get_current_user

router = APIRouter()

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("/", response_model=TodoSchemaPublic)
def create_todo(
    todo: TodoSchema,
    user: CurrentUser,
    session: Session,
):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.get("/", response_model=TodoSchemaList)
def list_todos(
    session: Session,
    user: CurrentUser,
    todo_filter: Annotated[FilterTodo, Query()],
):

    query = select(Todo).where(Todo.user_id == user.id)

    if todo_filter.title:
        query = query.filter(Todo.title.contains(todo_filter.title))

    if todo_filter.description:
        query = query.filter(Todo.description.contains(todo_filter.description))

    if todo_filter.state:
        query = query.filter(Todo.state == todo_filter.state)

    todos = session.scalars(
        query.offset(todo_filter.offset).limit(todo_filter.limit)
    ).all()

    return {"todos": todos}


@router.patch("/{todo_id}", response_model=TodoSchemaPublic)
def patch_todo(
    user: CurrentUser,
    session: Session,
    todo_id: int,
    todo: TodoSchemaUpdate,
):
    db_todo = session.scalar(
        select(Todo).where(Todo.id == todo_id, Todo.user_id == user.id)
    )

    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Task not found.",
        )

    for field, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, field, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.delete("/{todo_id}", response_model=MessageSchema)
def delete_todo(
    todo_id: int,
    user: CurrentUser,
    session: Session,
):
    todo = session.scalar(
        select(Todo).where(Todo.id == todo_id, Todo.user_id == user.id)
    )

    if not todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Task not found.",
        )
    session.delete(todo)
    session.commit()
    return {"message": "Task has been deleted successfully."}
