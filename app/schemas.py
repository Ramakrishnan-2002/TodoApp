from pydantic import BaseModel,EmailStr
from datetime import datetime 

class User_create(BaseModel):
    username :str
    email : EmailStr
    password : str
    role :str
    ph_number : str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenResponseData(BaseModel):
    id :int

class UserOut(BaseModel):
    username : str
    email : EmailStr
    id : int
    
class PasswordVerification(BaseModel):
    new_password:str

class TodoRequest(BaseModel):
    title: str
    completed : bool
    priority : int

class TodoResponse(BaseModel):
    id : int
    title: str
    completed : bool
    priority : int
    owner_id : int
    created_at : datetime
    owner : UserOut
    class Config:
        from_attributes=True