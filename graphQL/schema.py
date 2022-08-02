from tokenize import String
from graphene import ObjectType, String, Int, Field, Schema, List
from models import Person, data
#Make a class defining our data model

"""
    class PersonType:
        email:str
        first_name:str
        last_name:str
        age:int
"""

class PersonType(ObjectType):
    email=String()
    first_name=String()
    last_name=String()
    age=Int()

    #resolvers
    def resolve_email(person, info):
        return person.email
    
    def resolve_fname(person, info):
        return person.first_name
    
    def resolve_lname(person, info):
        return person.last_name
    
    def resolve_age(person, info):
        return person.age


class Query(ObjectType):
    all_people=List(PersonType)
    person=Field(PersonType, key=Int())

    def resolve_all_people(root, info):
        return data.values()
    
    def resolve_person(root, info, key):
        return data[key]

    

schema = Schema(query=Query)



#query
#query_string="{allPeople{email lastName firstName}}"

#print(schema.execute(query_string))