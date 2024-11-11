from fastapi import FastAPI,Request,status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from .routers import todo,users,auth,admin
from . import models
from .database import engine
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()
origins=["*"] #we can specify which domain we can use 


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



models.Base.metadata.create_all(bind=engine)
app.mount("/static",StaticFiles(directory="app/static"),name="static")


@app.get("/")
async def test(request:Request):
    return RedirectResponse(url="/todos/todo-page",status_code=status.HTTP_302_FOUND)

app.include_router(todo.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(admin.router)
 