from fastapi import APIRouter,Depends,HTTPException,status,Path
from ..database import db_dependency
from ..OAuth2 import get_current_user,verify_access_token
from ..models import Todo, User
from ..schemas import TodoRequest,Token

router=APIRouter(
    prefix="/todos",
    tags=['todos']
)

#pages



def redirect_to_login():
    redirect_response=RedirectResponse(url="/users/login-page",status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response


from fastapi import Request
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
templates=Jinja2Templates(directory="app/templates")
@router.get("/todo-page")
async def render_todo_page(request: Request, db: db_dependency):
    try:
        # Retrieve and wrap the token from cookies
        token_value = request.cookies.get("access_token")
        if not token_value:
            return redirect_to_login()
        
     

        # Verify token
        user_id =  verify_access_token(
            token=token_value,
            credentials_exception=HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        )
        
        # Query todos for the user
        todos = db.query(Todo).filter(Todo.owner_id == user_id.id).all()
        user=db.query(User).filter(User.id==user_id.id).first()
    
        return templates.TemplateResponse("todo.html", {"request": request, "todos": todos, "user": user})

    except Exception as e:
        print(f"Error verifying token: {e}")
        return redirect_to_login()

@router.get("/add-todo-page")
async def render_todo_page(request: Request,db:db_dependency):
    try:
        token_value = request.cookies.get("access_token")
    
        if not token_value:
            return redirect_to_login()
        user_id =  verify_access_token(
            token=token_value,
            credentials_exception=HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        )
        
        user=db.query(User).filter(User.id==user_id.id).first()
        if user is None:
            return redirect_to_login()
        return templates.TemplateResponse("add-todo.html",{"request":request,"user":user})
    except :
        return redirect_to_login()
    
@router.get("/edit-todo-page/{t_id}")
async def render_todo_page(request:Request,t_id:int,db:db_dependency):
    try:
        # Retrieve and wrap the token from cookies
        token_value = request.cookies.get("access_token")
        if not token_value:
            return redirect_to_login()
        
     
        
        # Verify token
        user_id =  verify_access_token(
            token=token_value,
            credentials_exception=HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        )
        
        # Query todos for the user
        todos = db.query(Todo).filter(Todo.id==t_id).all()
        user=db.query(User).filter(User.id==user_id.id).first()
        return templates.TemplateResponse("edit-todo.html", {"request": request, "todo": todos, "user": user})
    except :
        return redirect_to_login()















#endpoints
@router.post("/createtodo",status_code=status.HTTP_201_CREATED)
async def create(db:db_dependency,val:TodoRequest,user=Depends(get_current_user)):
    todo_model=Todo(owner_id=user.id,**val.model_dump())
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)

@router.get("/",status_code=status.HTTP_200_OK)
async def get_all_todos(db:db_dependency,user=Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorised user")
    todo_model=db.query(Todo).all()
    return todo_model


@router.get("/getwithuserid",status_code=status.HTTP_200_OK)
async def getbyuserid(db:db_dependency,user=Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorised user")
    todo_model=db.query(Todo).filter(Todo.owner_id==user.id).first()
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Todos not found in the current user")
    return todo_model

@router.put("/{t_id}",status_code=status.HTTP_200_OK)
async def update_todo(db:db_dependency,val:TodoRequest,t_id:int=Path(gt=0),user=Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorised user")
    todo_model=db.query(Todo).filter(Todo.owner_id==user.id).filter(Todo.id==t_id).first()
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Todo does not exist")
    todo_model.title=val.title
    todo_model.completed=val.completed
    todo_model.priority=val.priority
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)

@router.delete("/delete/{t_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete(db:db_dependency,t_id:int=Path(gt=0),user=Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorised user")
    todo_model=db.query(Todo).filter(user.id==Todo.owner_id).filter(Todo.id==t_id).first()
    db.delete(todo_model)
    db.commit()