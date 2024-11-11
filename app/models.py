from .database import Base
from sqlalchemy import Integer,String,Column,Boolean,TIMESTAMP,ForeignKey, func
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__="users"
    id = Column(Integer,primary_key=True,index=True,nullable=False)
    username=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    role=Column(String,nullable=False)
    ph_number=Column(Integer,nullable=False,unique=True)
    created_at=Column(TIMESTAMP(timezone=True),nullable=True,server_default=func.now())


class Todo(Base):
    __tablename__="Todos"
    id=Column(Integer,primary_key=True,nullable=False,index=True)
    title=Column(String,nullable=False)
    completed=Column(Boolean,nullable=False)
    priority=Column(Integer,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=True,server_default=func.now())
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    owner=relationship("User")