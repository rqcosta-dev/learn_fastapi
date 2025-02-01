from http import HTTPStatus
from fastapi import FastAPI
from fast_zero.schemas import Message
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)  # 200 OK
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
