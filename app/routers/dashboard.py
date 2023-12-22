from .. import models,schemas,utils
from fastapi import Body, FastAPI, Request, Response, status, HTTPException, APIRouter
from random import randrange
from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import Depends
from ..database import get_db
from .. import oauth2
from sqlalchemy import func
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


router = APIRouter(
    prefix="/dashboard",
    tags=['Dashboard'],
)


@router.get("/", response_model=List[schemas.PostOut])
def get_user_posts(request: Request, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user),limit: int = 10, skip:int = 0, search: Optional[str] =""):
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search),models.Post.owner_id == current_user.id).limit(limit).offset(skip).all()

    return templates.TemplateResponse("dashboard.html", {"request": request, "posts": posts})
    #return posts
