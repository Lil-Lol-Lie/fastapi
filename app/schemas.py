"""Set rules for user input and output"""
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional, Literal

class PostBase(BaseModel): #rules check
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

#handle info sending back to users
class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: UserOut
    class Config:
        orm_mode = True
        
class PostOut(BaseModel):
    Post: Post
    votes: int
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) #Literal[0,1]