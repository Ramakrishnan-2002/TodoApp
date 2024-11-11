from fastapi import APIRouter,Depends,HTTPException,status
from ..schemas import UserOut,TodoResponse
from ..database import db_dependency
from ..OAuth2 import get_current_user
from ..models import User,Todo

router=APIRouter(
    prefix="/admin",
    tags=['admin']
)



@router.get("/getalltodos",response_model=list[TodoResponse])
async def getalltodos(db:db_dependency,user=Depends(get_current_user)):
    if user.role !='admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not authorised to admin previleges")
    todos=db.query(Todo).all()
    if todos is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Todos not found")
    return todos





@router.get("/getallusers",response_model=list[UserOut])
async def get_all_users(db:db_dependency,user =Depends(get_current_user)):
    if user.role !='admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not authorised to admin previleges")
    users=db.query(User).all()
    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Users not found")
    return users 

 