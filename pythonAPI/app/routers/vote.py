from email.policy import HTTP
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..schemas import Vote
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from ..database import SessionLocal, engine, get_db

router = APIRouter(
    prefix='/vote',
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} not found")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.uid)

    found_vote = vote_query.first()
    
    if vote.direction == 1:
        if found_vote:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail=f"user {current_user.uid} has already voted on post {vote.post_id}")
        
        
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.uid)
        db.add(new_vote)
        db.commit()

        return {"message" : "sucessfully added votes!"}
    else:

        if not found_vote:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")

        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message" : "succesfully deleted the vote!"}
