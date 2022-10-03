from audioop import cross
from email.mime import base
from lib2to3.pytree import Base
from pydantic import BaseModel, Field
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import sqlalchemy_db
from sqlalchemy_db import Crossover_project, engine

app = FastAPI()

sqlalchemy_db.base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = sqlalchemy_db.get_session()
        yield db
    finally:
        db.close()

class Cross(BaseModel):
    password: str
    cpu: Optional[str]
    user: str 
    mail: str
    ip: str
    RAMmemory: str

@app.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(sqlalchemy_db.Crossover_project).all()

@app.get("/crossover_project/{cross_id}")
async def read_cross(cross_id: int, db: Session = Depends(get_db)):
    cross_model = db.query(sqlalchemy_db.Crossover_project)\
        .filter(sqlalchemy_db.Crossover_project.id == cross_id)\
        .first()
    if cross_model is not None:
        return cross_model
    raise http_exception()

@app.post("/")
async def create_cross(cross: Cross, db: Session = Depends(get_db)):
    cross_model = sqlalchemy_db.Crossover_project()
    cross_model.password = cross.password
    cross_model.cpu = cross.cpu
    cross_model.user = cross.user
    cross_model.mail = cross.mail
    cross_model.ip = cross.ip
    cross_model.RAMmemory = cross.RAMmemory

    db.add(cross_model)
    db.commit()

    return successful_response(200)



@app.put("/{cross_id}")
async def update_cross(cross: Cross, cross_id: int, db: Session = Depends(get_db)):
    cross_model = db.query(sqlalchemy_db.Crossover_project)\
        .filter(sqlalchemy_db.Crossover_project.id == cross_id)\
        .first()
    if cross_model is None:
        raise http_exception()
    
    cross_model.password = cross.password
    cross_model.cpu = cross.cpu
    cross_model.user = cross.user
    cross_model.mail = cross.mail
    cross_model.ip = cross.ip
    cross_model.RAMmemory = cross.RAMmemory

    db.add(cross_model)
    db.commit()

    return successful_response(200)


@app.delete("/{cross_id}")
async def delete_cross(cross_id: int, db: Session = Depends(get_db)):
    cross_model = db.query(sqlalchemy_db.Crossover_project)\
        .filter(sqlalchemy_db.Crossover_project.id == cross_id)\
        .first()
 
    if cross_model is None:
        raise http_exception()


    db.query(sqlalchemy_db.Crossover_project)\
    .filter(sqlalchemy_db.Crossover_project.id == cross_id)\
    .delete()

    db.commit()

    return successful_response(200)



def successful_response(status_code: int):
    return {
        'status': status_code, 
        'transaction': 'Successful'
    }
    

def http_exception():
    return HTTPException(status_code=404, detail="Todo not found")


    
    