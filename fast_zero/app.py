from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fast_zero.models import User

from http import HTTPStatus
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fast_zero.database import get_session
from fast_zero.schemas import (
    MessageSchema,
    UserSchema,
    UserSchemaPublic,
    UserSchemaList,
)

app = FastAPI()


@app.get("/", status_code=HTTPStatus.OK, response_model=MessageSchema)  # 200 OK
def read_root():
    return {"message": "Hello World!"}


@app.get("/web-page", status_code=HTTPStatus.OK, response_class=HTMLResponse)
def response_html():
    return """
    <html>
        <head>
            <title>FastAPI</title>
        </head>
        <body>
            <h1>Hello World!</h1>
        </body>
    </html>
    """


@app.post(
    "/users/", status_code=HTTPStatus.CREATED, response_model=UserSchemaPublic
)  # 201 Created
def create_user(user: UserSchema, session: Session = Depends(get_session)):
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

    db_user = User(username=user.username, email=user.email, password=user.password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get("/users/", status_code=HTTPStatus.OK, response_model=UserSchemaList)
def read_user(
    limit: int = 10,
    skip: int = 0,
    session: Session = Depends(get_session),
):
    user = session.scalars(select(User).limit(limit).offset(skip))
    return {"users": user}


@app.put("/users/{user_id}", status_code=HTTPStatus.OK, response_model=UserSchemaPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session = Depends(get_session),
):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    try:
        db_user.username = user.username
        db_user.email = user.email
        db_user.password = user.password
        session.commit()
        session.refresh(db_user)

        return db_user
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Username or Email already exists"
        )


@app.delete("/users/{user_id}", response_model=MessageSchema)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    session.delete(db_user)
    session.commit()
    return {"message": "User deleted successfully"}


@app.get("/users/{user_id}", status_code=HTTPStatus.OK, response_model=UserSchemaPublic)
def read_user_by_id(
    user_id: int,
    session: Session = Depends(get_session),
):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    return db_user
