from http import HTTPStatus
from fastapi import FastAPI, HTTPException
from fast_zero.schemas import (
    MessageSchema,
    UserSchema,
    UserSchemaPublic,
    UserDB,
    UserSchemaList,
)
from fastapi.responses import HTMLResponse

app = FastAPI()

database = []


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
def create_user(user: UserSchema):
    user_with_id = UserDB(id=len(database) + 1, **user.model_dump())

    database.append(user_with_id)
    return user_with_id


@app.get("/users/", status_code=HTTPStatus.OK, response_model=UserSchemaList)
def read_user():
    user = {"users": database}
    return user


@app.put("/users/{user_id}", status_code=HTTPStatus.OK, response_model=UserSchemaPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )  # 404 Not Found

    user_index = user_id - 1
    user_with_id = UserDB(id=user_id, **user.model_dump())
    database[user_index] = user_with_id
    return user_with_id


@app.delete("/users/{user_id}", response_model=MessageSchema)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    user_index = user_id - 1
    del database[user_index]
    return {"message": "User deleted successfully"}


@app.get("/users/{user_id}", status_code=HTTPStatus.OK, response_model=UserSchemaPublic)
def read_user_by_id(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    user_index = user_id - 1
    return database[user_index]
