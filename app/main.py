from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app import oauth2

from app.oauth2 import get_current_user
from . import models
from . database import engine
from .routers import post, user, auth, vote, dashboard
from fastapi.staticfiles import StaticFiles



#models.Base.metadata.create_all(engine)
origins = ["*"]

app = FastAPI()
templates = Jinja2Templates(directory="templates")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/",name="mainpage")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "name": "FastAPI User"})


@app.get("/users.html", response_class=HTMLResponse)
def users_page():
    return FileResponse("templates/users.html")

@app.get("/create_post.html", response_class=HTMLResponse)
def create_posts_page():
    return FileResponse("templates/create_post.html")





app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(dashboard.router)