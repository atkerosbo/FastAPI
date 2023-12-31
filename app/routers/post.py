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
    prefix="/posts",
    tags=['Posts'],
)

#get all posts

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(request: Request, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip:int = 0, search: Optional[str] =""):

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #posts = list ( map (lambda x : x._mapping, results) )
    return templates.TemplateResponse("posts.html", {"request": request, "posts": posts})
    #return posts

#get users posts  
@router.get("/user/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    
    return posts 

#create new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post )
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


#get specific post with id
@router.get("/{id}", response_model=schemas.PostOut, name ='get_single_post')
def get_post(request: Request, id:int,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    print(post)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return templates.TemplateResponse("post.html", {"request": request, "post": post})
    #return post


#update posts
@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, post:schemas.PostBase,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_old = post_query.first()

    if post_old == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    if post_old.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post_query.update(post.model_dump(), synchronize_session=False)

    db.commit()
    return post_query.first()

#delete posts
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post_query.delete(synchronize_session=False) 
    db.commit() 
    return {"message": f"Post with id {id} deleted"}
