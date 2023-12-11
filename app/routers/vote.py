from .. import models,schemas,utils, oauth2
from fastapi import Body, FastAPI, Response, status, HTTPException, APIRouter
from random import randrange
from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import Depends
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags=['Votes']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} does not exist")
    
    vote_query = db.query(models.Post).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    
    delete_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    if (vote.dir == 1):
       if found_vote:
           raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
       new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
       db.add(new_vote)
       db.commit()
       return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

        delete_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}    