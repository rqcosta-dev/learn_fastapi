from http import HTTPStatus
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fast_zero.schemas import MessageSchema

from fast_zero.routers import auth, users

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)


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
