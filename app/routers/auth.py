from typing import Annotated
from fastapi import APIRouter,HTTPException,status,Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.OAuth2 import create_access_token
from ..database import db_dependency
from ..models import User
from ..utils import verify
from ..schemas import Token

router=APIRouter(
    prefix="/login",
    tags=['Authentication']
)



















#Endpoints
@router.post("/token",status_code=status.HTTP_200_OK,response_model=Token)
async def login(user_cred:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    user=db.query(User).filter(user_cred.username==User.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User not found")
    if not verify(user_cred.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User not found")
    
    #creating token
    access_token=create_access_token(data={"user_id":user.id})
    return {"access_token":access_token,"token_type":"bearer"}