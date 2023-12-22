from typing import List
from fastapi import APIRouter, Depends, status, Response
from fastapi.responses import JSONResponse, RedirectResponse  # Import RedirectResponse

from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, utils, schemas, database, oauth2
from fastapi import HTTPException
from numpy import random

templates = Jinja2Templates(directory="templates")


sessions = {}
router = APIRouter(
    tags=["Authentication"]
)

#@router.post('/login', response_model=schemas.Token)
@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create a token
    # return token

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    #set the token to a session cookie
    response = RedirectResponse(url="/dashboard")  # Use RedirectResponse for redirection
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)

    #return templates.TemplateResponse("dashboard.html", {"response": response, "name": "user"})
    #return response
    return {"access_token": access_token, "token_type": "bearer"}

