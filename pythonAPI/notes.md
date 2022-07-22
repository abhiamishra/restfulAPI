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