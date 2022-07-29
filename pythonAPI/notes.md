# Python Virtual Environments
Let's say we have a project that requires a certain version.

Now, another project requires a newer version. Now, you
have to upgrade on local machine.

This may or may not be a problem...

To solve this, we create a virtual environment that won't affect any other environment and we can install packages that don't affect anything else!

# Analyzing FastAPI
Path Operation: also referred to as route (think Flask)

has two components: function and decorator
The function is pretty much the same as functions in pytho - nothing too crazy. Whatever is returned from function is what is returned back to the user.

JSON is the main universal language for APIs.

A decorator to a function, it performs a little magic ->
allows our functions to turn into an path operation. Without it, the functions are just,,,functions!

The decorator contains a path -> this is the path right after the domain and this path (and its differences) allow for us to navigate to different routes, webpages, and APIs.

# Post Requests v. Get Request
Get request: Send an HTTP Request to API and we simply send data to the client

Post request: When we send our HTTP request, we also send data! and then API sends some data back to the client.

# Why We Need Schema for APIs
- It's a pain to get all values from body
- Client can send whatever data they want
- Data doesn't get validated
- Ultimately, we want to force the client to send data in a schema that we expect

# CRUD Operations
Standard convention is for a resource, use plural names (posts not post, users not user)
- C reate [POST]
- R ead [GET] -> get ALL or get by id
- U pdate [PUT/PATCH] -> update by id (PUT replaces the entire resource while PATCH replaces a simple field in the resource)
- D elete [DELETE] -> delete by id
- Path ordering matters!


# Databases and API
- Database = collection of organized data that can be esaily accessed and managed
- We use a DBMS that allows us to interact with the database management system
- Postgres => each instance of postgres can be carved into multiple separate databses
    - each Postgres installation comes w one database called postgres since you need to connect to a database to access anything.
- a table represents a subject or event in an application
- Column represents a different attribute
- Row represents a different entry in the table
- Databases have data types
- Primary Key: a column or a group of columns that uniquely identifies each row in a table.
- Table can only have one and only one primary key
    - entries must be unique and no duplicates
- NULL Constrains
    - by default, any column can be left blank - it has null value
    - a NOT NULL constraint requires a field to be filled in



# Object Relational Mapper (ORM)
- Layer of abstraction that sits between the database and us
- We can perform all databsae operations through traditional python code
    - aka converts our python code to SQL statements that then gets delivered to our database
- Instead of manually defining tables, we can define tables as python models
- Additionally, queries can be made through the python code so that no SQL is necessary
- SQLAlchemy is an example of a python ORM
    - Standalone library and has no association with FastAPI
    - Can be used with other Python web frameworks
- Always be sure to download the underlying database driver since the driver is what talks to the SQL ultimately - the ORM is just a level of abstraction between the user and the database driver
- SQLAlchemy can generate tables but in a simple manner
- If the table already exists with the name there, it won't modify the tables! Only useful for creating it once


# Difference between Schema/Pydantic Model and ORM Model
- Schema for a Pydantic Model => defines schema for how the USER has to shape a request. Allows us to shape the format of request
    - Defines structure of a request and response
    - Ensures that when a user creates the psost, the request will only go through if it has a title and content in the model.
    - The pydantic model serves as a validation schema for the API calls between server and client.
- Schema for ORM Model => defines how our table/database looks like
    - Responsible for defining the columns of our "posts" table
    - Is used to query, create, delte, and update entries within the database

# JWT Token Authentication
- Authentication with an API: Session Based
    - Store on our backend and track whether a user is logged in
    - either stored in memory or database when user logs in or logs out
- Other way: JWT Token
    - it is stateless
    - NOTHING in our backend that will keep track whether a user is logged in or logged out
    - token itself, we don't store, is stored on our client side and keeps track of whether it is logged in / logged out
- How it works:
    - Client tries to login with username and password
    - API receives that
        - if credentials are valid, we create a JWT Token
        - we send a response back with the token
    - Now he has the token and can access our applications (get posts, etc)
        - BUT he has also to provide the JWT token when they send the request
    - When API receives it:
        - verifies that token is valid
        - then we send back data.
    - That's it!

# JWT Deep Dive
- It is not encrypted
- Has three components
    1. Header: provide a hashing algorithm and specify type of taken (JWT in this case)
    2. Payload: data that the token holds. Be careful w what you put because token is not encrypted. More information also means token size becomes large
    3. Signature: Take the header and payload nad add a SECRET (a special password that only the API knows!) and use the hashing algorithm we used in the header to create a signature.


# Purpose of Signature
- User login has:
    - Header
    - Payload
    - Secret
- Those three get combined into JWT Token's signature which also adds:
    - a header and a payload
    - Token's header and payload = JWT Token's header and payload
- Now we have a TOKEN!

- Let's say we have a hacker and goes through our token and makes the role of the user be ADMIN
- He now tries to login which generates a token
- However, he doesn't have a SECRET and as such, he can't generate an updated signature
    - In essence, the signature that he has doesn't match the data he has
    - He can't create the signature because he doesn't have access to our SECRET since its only on OUR API SERVER

- The API takes the header, the payload and secret and creates a test signature
    - We take the test signature and match it up with the signature of the token
    - If they don't match, then authentication is NOT VALID!
    - Signature ENSURES data integrity is valid!


# Logging in a User
- User goes to login page and sends email password
- API receives it, finds user by email, and retrieves the hashed password
- We take user provided password and hash that -> test_hashed_password
- Now if test_hashed_password == hashed_password, we're in!


# Relationships
- Currently we have two separate tables: Users and Posts
- We create a foreign key -> how we tell SQL how one table is connected to another
    - we specify the table it should be connected to
    - we specify the id in that table we need to be connected to
- Whenever we create a post, we embed a special id for that user with that post and we're linked between posts and users!

# Voting/Likes System Requirements
- Users should be able to like a post
- Should only be able to like a post once
- Retrieving posts shold also fetch the total number of likes

# Vote Model
- Column referencing the post id
- Column referencing the id of user who liked the post
- A user should only be able to like a post once so this means we need to ensure every post_id / voter_id is an unique combo.

# Composite Keys
- Primary Key => spans multiple columns
- Since primary keys must be unique, this will ensure that no user can like a post twice


# Vote Route
- path will be at /vote
- user id will be extracted from the JWT token
- body will contain id of the post the user is voting on + direction of vote
- 1 => add a vote while 0 => delete a vote

# Database Migration with Alembic
- able to create incremental changes to database and track it
- Developers can track changes to code and rollback code easily with GIT -> why not do the same w database models
- Database migrations allow to incrementally track changes to schema and rollback changes to any point in time
- Alembic is the tool
- Alembic can automatically pull database models from SQLAlchemy and generate the proper tables
- upgrade() -> runs commands for creating databases
- downgrade() -> handle removing tables, creation, rolling it back
    - both are essentially manual

# Pre - Deployment Checklist
- POSTMAN only sends requests from your own computer


