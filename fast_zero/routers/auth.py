from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.models import User
from fast_zero.database import get_session
from fast_zero.security import verify_password, create_access_token, get_current_user
from fast_zero.schemas import TokenSchema

router = APIRouter(prefix="/auth", tags=["auth"])

T_Session = Annotated[Session, Depends(get_session)]
T_Oauth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post("/token", status_code=HTTPStatus.OK, response_model=TokenSchema)
def login_access_token(
    session: T_Session,
    form_data: T_Oauth2Form,
):
    db_user = session.scalar(select(User).where(User.email == form_data.username))

    if not db_user or not verify_password(form_data.password, db_user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Incorrect email or password"
        )
    access_token = create_access_token(data={"sub": db_user.email})

    return {"access_token": access_token, "token_type": "Bearer"}


@router.post("/refresh_token", status_code=HTTPStatus.OK, response_model=TokenSchema)
def refresh_access_token(user: User = Depends(get_current_user)):
    new_access_token = create_access_token(data={"sub": user.email})

    return {"access_token": new_access_token, "token_type": "Bearer"}
