from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

#Response model
class UserOut(BaseModel):
    uid: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

#Defining schema for Post
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

#inherits fields from PostBase
class PostCreate(PostBase):
    pass 


#Defining schema for Response
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int
    
    class Config:
        orm_mode = True


#Response schema for JWT
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    

class Vote(BaseModel):
    post_id: int
    direction: conint(le=1)
