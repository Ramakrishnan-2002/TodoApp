from fastapi import APIRouter,Depends,HTTPException,status
from ..database import db_dependency
from .. import models,utils
from ..schemas import User_create,UserOut,PasswordVerification
from ..models import User
from ..OAuth2 import get_current_user
from ..utils import hash

router=APIRouter(
    tags=['users'],
    prefix="/users"
)


#Pages
from fastapi import Request
from fastapi.templating import Jinja2Templates
templates=Jinja2Templates(directory="app/templates")

@router.get("/login-page")
async def render_login_page(request:Request):
    return templates.TemplateResponse("login.html",{"request":request})
@router.get("/register-page")
async def render_register_page(request:Request):
    return templates.TemplateResponse("register.html",{"request":request})

@router.post("/createuser")
async def create_user(new_user : User_create,db:db_dependency):
    new_user.password=utils.hash(new_user.password)
    user_model= models.User(**new_user.model_dump())
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model



@router.post("/changepassword")
async def chgpwd(db:db_dependency,pwdchange_data:PasswordVerification,user=Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    user.password= hash(pwdchange_data.new_password)
    db.add(user)
    db.commit()
