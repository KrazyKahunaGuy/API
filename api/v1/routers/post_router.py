"""
This handles routes concerned with the creation, fetching, modification, and deletion of posts.
"""

from typing import List

from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from api.v1 import dependencies

from api.v1.db.dals import post_dal, user_dal
from api.v1.schemas import post_schemas

security = HTTPBearer()

router = APIRouter(prefix="/posts", tags=['Posts'])


@router.post("/user/", response_model=post_schemas.Post)
def create_post(post: post_schemas.PostCreate, db: Session = Depends(dependencies.get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    access_token = credentials.credentials
    user_id = user_dal.get_user_by_username(
        db=db, username=user_dal.auth_handler.decode_token(access_token)).id
    db_post = post_dal.create_post(db=db, owner_id=user_id, post=post)
    return db_post


@router.get("/user/", response_model=List[post_schemas.Post])
def get_user_posts(owner_id: int, db: Session = Depends(dependencies.get_db), skip: int = 0, limit: int = 100):
    db_user_posts = post_dal.get_user_posts(
        db=db, user_id=owner_id, skip=skip, limit=limit)
    return db_user_posts


@router.get("/", response_model=List[post_schemas.Post])
def get_all_posts(db: Session = Depends(dependencies.get_db), skip: int = 0, limit: int = 100):
    db_all_posts = post_dal.get_all_posts(db=db, skip=skip, limit=limit)
    return db_all_posts


@router.get("/user/post/", response_model=post_schemas.Post)
def get_user_post(owner_id: int, post_id: int, db: Session = Depends(dependencies.get_db)):
    db_user_post: dict = post_dal.get_user_post(
        db=db, user_id=owner_id, post_id=post_id)
    return db_user_post


@router.get("/post/", response_model=post_schemas.Post)
def get_a_post(post_id: int, db: Session = Depends(dependencies.get_db)) -> dict:
    db_get_a_post: dict = post_dal.get_a_post(db=db, post_id=post_id)
    return db_get_a_post


@router.put("/user/post/", response_model=post_schemas.Post)
def update_post(post_id: int, post: post_schemas.PostUpdate, db: Session = Depends(dependencies.get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    access_token = credentials.credentials
    user_id = user_dal.get_user_by_username(
        db=db, username=user_dal.auth_handler.decode_token(access_token)).id
    db_update_post = post_dal.update_post(
        db=db, user_id=user_id, post_id=post_id, post=post)
    return db_update_post


@router.delete("/user/post/", response_model=post_schemas.Post)
def delete_post(post_id: int, db: Session = Depends(dependencies.get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    access_token = credentials.credentials
    user_id = user_dal.get_user_by_username(
        db=db, username=user_dal.auth_handler.decode_token(access_token)).id
    db_delete_post = post_dal.delete_post(
        db=db, user_id=user_id, post_id=post_id)
    return db_delete_post
