import datetime
from typing import List

from pydantic import BaseModel

from api.v1.schemas.comment_schemas import Comment


class PostBase(BaseModel):
    title: str
    body: str


class PostCreate(PostBase):
    pass

    class Config:
        schema_extra = {
            "example": {
                "title": "Hello World",
                "body": "This is my first post",
            }
        }


class PostUpdate(PostCreate):
    pass


class Post(BaseModel):
    id: int
    title: str
    body: str
    owner_id: int
    created: datetime.datetime
    last_modified: datetime.datetime

    comments: List[Comment] = None

    class Config:
        orm_mode = True
