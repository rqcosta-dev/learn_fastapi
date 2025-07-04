from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.security import get_password_hash, get_current_user
from fast_zero.schemas import (
    MessageSchema,
    UserSchema,
    UserSchemaPublic,
    UserSchemaList,
)

router = APIRouter(prefix="/users", tags=["users"])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("/", status_code=HTTPStatus.OK, response_model=UserSchemaList)
def read_user(
    session: T_Session,
    limit: int = 10,
    skip: int = 0,
):
    user = session.scalars(select(User).limit(limit).offset(skip))
    return {"users": user}


@router.get("/{user_id}", status_code=HTTPStatus.OK, response_model=UserSchemaPublic)
def read_user_by_id(
    session: T_Session,
    user_id: int,
):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    return db_user


@router.put("/{user_id}", status_code=HTTPStatus.OK, response_model=UserSchemaPublic)
def update_user(
    session: T_Session,
    current_user: T_CurrentUser,
    user_id: int,
    user: UserSchema,
):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="You don't have permission to update this user",
        )
    try:
        current_user.username = user.username
        current_user.email = user.email
        current_user.password = get_password_hash(user.password)
        session.commit()
        session.refresh(current_user)

        return current_user
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Username or Email already exists",
        )


@router.delete("/{user_id}", response_model=MessageSchema)
def delete_user(
    session: T_Session,
    current_user: T_CurrentUser,
    user_id: int,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="You don't have permission to delete this user",
        )

    session.delete(current_user)
    session.commit()
    return {"message": "User deleted successfully"}


@router.post(
    "/", status_code=HTTPStatus.CREATED, response_model=UserSchemaPublic
)  # 201 Created
def create_user(session: T_Session, user: UserSchema):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="Username already exists"
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="Email already exists"
            )

    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
