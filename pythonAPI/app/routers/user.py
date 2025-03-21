from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..schemas import PostBase, PostCreate, Post, UserCreate
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import SessionLocal, engine, get_db

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


########### ROUTES FOR USERS ###################
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #hash the password
    hashed_password = utils.hashIt(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()

    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.uid == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"User with id: {id} did not exist")
    return user

