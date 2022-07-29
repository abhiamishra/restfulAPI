from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from.config import settings



#models.Base.metadata.create_all(bind=engine) #With Alembic, this command is not as necessary

app = FastAPI()

#all domains that can talk to our API
origins = ["*"] # * = wildcard

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


#Decorator
@app.get("/")
#Function for the decorator
def root():
    return {"message": "Welcome to My API"}
