from fastapi import FastAPI
import graphql
from schema import schema
import starlette
import graphene
import starlette
import graphql
from starlette.applications import Starlette
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

app=FastAPI()

app.add_route('/graphql', GraphQLApp(schema=schema, on_get=make_graphiql_handler()))



@app.get('/')
async def index():
    return {"message" : "Yo"}