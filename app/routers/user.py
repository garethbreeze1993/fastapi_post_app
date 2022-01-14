from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import exc

from app import models
from app.database import engine, get_db
from app.schemas import UserResponse, UserCreate
from app.utils import hash_password

router = APIRouter(prefix='/users', tags=['Users'])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # hash the password
    hashed_pwd = hash_password(user.password)
    user.password = hashed_pwd
    new_user = models.User(**user.dict())
    db.add(new_user)
    try:
        db.commit()
    except exc.SQLAlchemyError as e:
        # Handle error better
        return {'error', e}
    db.refresh(new_user)
    return new_user


@router.get("/{id_}", response_model=UserResponse)
def get_user(id_: int, db: Session = Depends(get_db)):
    user = db.query(models.User).get(id_)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post not found id={id_}')
    return user
