from email import contentmanager
from email.policy import HTTP
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

from setuptools import find_namespace_packages

app = FastAPI()

#Defining schema for Post
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{ "title": "title of post 1",
                "content": "content of post 1",
                "id": 1  },
            { "title": "Favorite Food",
                "content": "I like pizza",
                "id": 2  }]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] ==  id:
            return i
        

#Decorator
@app.get("/")
#Function for the decorator
def root():
    return {"message": "Welcome to My API"}

@app.get("/posts")
def get_posts():
    #array is automatically serialized
    return {"data": my_posts}

#Get post by a singular id
@app.get("/posts/{id}") #{id} is a path parameter
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found")
    return {"post_detail" : post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
#extract all fields from body and store them in dict
#def create_post(payload: dict = Body(...)):

#Here, we reference Schema by Pydantic
# - includes automatic validation for type and existence
def create_post(post: Post):
    #newPost is a Pydantic model object
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000000000)
    my_posts.append(post_dict) #Converts type to dictionary
    return {"data": post_dict} #When a post is created, send back the newly created psot


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting posts
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                                detail = f"post with id {id} doesn't exist!")
    my_posts.pop(index)

    #You don't want to send any data back - just a 204
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                                detail = f"post with id {id} doesn't exist!")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    
    return {"data" : post_dict}