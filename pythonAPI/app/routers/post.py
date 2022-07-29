from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from .. import oauth2
from ..schemas import PostBase, PostCreate, Post, UserCreate, PostOut
from .. import models, schemas, utils
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import SessionLocal, engine, get_db

# ROUTES: 

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user),
                limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #array is automatically serialized
    #WITH REGULAR RAW SQL: posts = find_all_posts()

    #WITH ORM: 
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
        #filter(models.Post.owner_id == current_user.uid).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Post.id==models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return results

#Get post by a singular id
@router.get("/{id}", response_model=schemas.PostOut) #{id} is a path parameter
def get_post(id: int, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    # WITH RAW SQL: post = find_post(id)

    # WITH ORM
    #post = db.query(models.Post).
    
    post = results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Post.id==models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found")
    
    #if(current_user.uid != post.owner_id):
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action!")
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
#extract all fields from body and store them in dict
#def create_post(payload: dict = Body(...)):

#Here, we reference Schema by Pydantic
# - includes automatic validation for type and existence
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    #newPost is a Pydantic model object
    #staged changes
    #WITH RAW SQL: 
    # new_post = post_one_post(post)
    # conn.commit()
    #committed changes



    #WITH ORM:
    new_post = models.Post(owner_id=current_user.uid, **post.dict())
    db.add(new_post)
    db.commit()

    db.refresh(new_post)
    return new_post #When a post is created, send back the newly created psot


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    # deleting posts
    #WITH RAW SQL: deleted_post = del_post(id)
     #Put in SQL statements
    
    # WITH ORM:
    deleted_query = db.query(models.Post).filter(models.Post.id==id)

    deleted_post = deleted_query.first()

    if deleted_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                                detail = f"post with id {id} doesn't exist!")
    
    if(current_user.uid == deleted_post.owner_id):
        deleted_query.delete(synchronize_session=False)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action!")

    #WITH RAW SQL: conn.commit()

    #You don't want to send any data back - just a 204
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    
    #WITH RAW SQL: updated_post = mod_post(id, post)
    updated_query = db.query(models.Post).filter(models.Post.id == id)

    updated_post = updated_query.first()

    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                                detail = f"post with id {id} doesn't exist!")
    if(current_user.uid == updated_post.owner_id):
           updated_query.update(post.dict(), synchronize_session=False)
           db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action!")
    #WITH RAW SQL:conn.commit()


    return updated_post