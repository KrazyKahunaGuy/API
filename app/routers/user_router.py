"""
This handles routes pertaining to creating, modiifying, logging in a user."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

import dependencies
import authentication
from db.dals import user_dal
# import schemas
from schemas import user_schemas

security = HTTPBearer()
auth_handler = authentication.Authentication()

router = APIRouter(prefix="/users")


@router.post("/", response_model=user_schemas.User)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    db_user = user_dal.get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Email is already registered")
    return user_dal.create_user(db=db, user=user)


@router.get("/refresh_token")
def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    refresh_token = credentials.credentials
    new_token = auth_handler.refresh_token(refresh_token)
    return {"access_token": new_token}


@router.get("/notasecret")
def not_a_secret():
    return "NOT A SECRET"


@router.get("/", response_model=List[user_schemas.User])
def get_users(db: Session = Depends(dependencies.get_db), skip: int = 0, limit: int = 100):
    db_users = user_dal.get_users(db, skip=skip, limit=limit)
    return db_users


@router.get("/{user_id}", response_model=user_schemas.User)
def get_user(user_id: int, db: Session = Depends(dependencies.get_db)):
    db_user = user_dal.get_user(db=db, user_id=user_id)
    return db_user


@router.post("/login", response_model=user_schemas.TokenData)
def login(credentials: user_schemas.Credentials, db: Session = Depends(dependencies.get_db)):
    db_user = user_dal.get_user_by_username(
        db=db, username=credentials.username)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect username")
    if not auth_handler.decode_password(credentials.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    access_token = auth_handler.encode_token(db_user.id)
    refresh_token = auth_handler.encode_refresh_token(db_user.id)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/secret")
def secret_data(credentials: HTTPAuthorizationCredentials = Security(security)):
    access_token = credentials.credentials
    if (auth_handler.decode_token(access_token)):
        return "SECRET DATA"