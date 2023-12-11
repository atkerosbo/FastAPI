from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from pydantic.types import conint




   
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
    

class PostCreate(PostBase):
    pass    

class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class Post(PostBase):
    created_at: datetime
    owner: UserOut
    id: int

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: str
    password: str

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True
  

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    

class TokenData(BaseModel):
    id: int

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)