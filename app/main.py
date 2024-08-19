from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from starlette.middleware.cors import CORSMiddleware
#from sqlalchemy.orm import declarative_base

#command tell SQLalchemy to run create statements to generate tables
#models.Base.metadata.create_all(bind=engine)
#Base = declarative_base()
app = FastAPI()

#function allows other domains access to our API
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
          
#split code to other file, and calling it here on main        
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/") #decorator turn into url api root path
def root():
    return {"message": "Hello World!!!"}