# What is GraphQL?
- GraphQL is a query language for your API
- In other APIs, you have a specific endpoint or URL that you hit that determines what data comes back
    - the API returns data in the form of JSON
- Aims to improve upon those ideas
- GraphQL allows you to ask for specific kinds of data and ask for what you want
    - instead of hitting an endpoint, you just ask (you query for it)
    - and you receive an object that contains what you need
- Allows for great relational queries
    - YouTube API and you get list of videos
        - you have to then go back and now w ids, you get messages
    - Now with GraphQL, you get the messages in one trip


- you write APIs as a series of type definitions and then you have some resolvers
- Server takes all of that and exposes that API via a single endpoint
- Client/User accesses that data through that singular endpoint.

# GraphQL v. REST for Side Projects
- Advantages of GraphQL
    - No over/under fetching of data
        - You can specify the fields and get exactly what you want
        - More complex to set up on the backend side
    - Don't have to version your API
    - It's a "type" system
        - allows you to catch errors, etc
- Disadvantages
    - More complex to fetch data 
    - Harder to cache and rate limit
    - Request monitoring


# Pictures of Final Product
![image](https://user-images.githubusercontent.com/52009380/182265030-a2c950cc-79d6-4842-94e9-7da9f18259bf.png)
![image](https://user-images.githubusercontent.com/52009380/182265036-34d9437a-5338-4043-959a-7d2087ecb6ae.png)
![image](https://user-images.githubusercontent.com/52009380/182265045-98ac5792-bc32-4ebb-b543-8c88a59d5055.png)

