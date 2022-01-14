from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import exc, and_

from app.database import engine, get_db
from app import models
from app import oauth2
from app.schemas import UserLogin, Token
from app.utils import hash_password, verify


router = APIRouter(tags=['Authentication'])


@router.post("/login", response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User)\
        .filter(models.User.email == user_credentials.username)\
        .first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')

    if not verify(plain_password=user_credentials.password, hashed_password=user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')

    # create token and return it
    access_token = oauth2.create_access_token(data=dict(user_id=user.id))
    return {'access_token': access_token, "token_type": "bearer"}
