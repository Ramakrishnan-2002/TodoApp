from typing import Annotated
from fastapi import status,HTTPException,Depends
import secrets
from datetime import datetime,timezone,timedelta
from jose import jwt,JWTError
from .schemas import TokenResponseData
from fastapi.security import OAuth2PasswordBearer
from .models import User
from sqlalchemy.orm import Session


SECRET_KEY=secrets.token_hex(32)
ALGORITHM= 'HS256'
TOKEN_EXPIRE_IN_MINUTES=30


def create_access_token(data):
    to_encode=data.copy()
    expires=datetime.now(timezone.utc)+timedelta(TOKEN_EXPIRE_IN_MINUTES)
    to_encode.update({"exp":expires})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id :str = payload.get("user_id")
        if not id:
            raise credentials_exception
        token_data=TokenResponseData(id=id)
        return token_data
    except JWTError:
        raise credentials_exception

from .database import db_dependency
oauth2_bearer=OAuth2PasswordBearer(tokenUrl='/login/token')
def get_current_user(db:db_dependency,token:str = Depends(oauth2_bearer)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not found")
    token_obj=verify_access_token(token,credentials_exception)
    user=db.query(User).filter(User.id==token_obj.id).first()
    return user

