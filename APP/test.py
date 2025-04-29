# """ 
# HTTP Method | Endpoint Name
# GET  | /
# GET  | /usersinfo
# GET  | /usersinfo/admin
# GET  | /usersinfo/recent_user
# GET  | /usersinfo/{place}
# POST | /adduser
# Delete | /usersinfo/delete/{name}
# """
# from fastapi import FastAPI, Response, status, HTTPException  # type: ignore
# from fastapi.params import Body  # type: ignore
# from pydantic import BaseModel  # type: ignore
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# # app = FastAPI()

        
# # -------------------------------------
# # Root endpoint - Simple welcome message
# # -------------------------------------
# @app.get("/")
# def Say_Hello():
#     """
#     This is the root endpoint. When accessed via a GET request,
#     it returns a simple message as a response indicating the first API endpoint.
#     """
#     return {"message": "first api"}

# # -------------------------------------
# # Pydantic model to validate user input
# # -------------------------------------
# PYDANTIC_MODEL = BaseModel
# class UserInfo(PYDANTIC_MODEL):
#     """
#     Pydantic model to define the structure of user data.
#     This ensures that the data coming to the API is validated and properly formatted.
#     """
#     name: str  # User's name (Required)
#     age: int  # User's age (Required)
#     place: str  # User's place of residence (Required)
#     graduation: bool = False  # Whether the user has completed graduation (Optional, defaults to False)
#     admin_privileges: bool = False  # Whether the user has admin privileges (Optional, defaults to False)

# # -------------------------------------
# # In-memory data storage (mock DB)
# # -------------------------------------
# post_data = [
#     {"name": "prasanna", "age": 23, "place": "Guntur", "graduation": True, "admin_privileges": True},
#     {"name": "sai", "age": 12, "place": "Chennai", "graduation": False,},
#     {"name": "suresh", "age": 25, "place": "guntur", "graduation": True,"admin_privileges": True},
#     {"name": "kiran", "age": 20, "place": "Guntur", "graduation": False},
#     {"name": "Murthy", "age": 23, "place": "Hydrabad", "graduation": True},
# ]
# """
# In-memory data storage (a list of dictionaries) used as a mock database for user data.
# In real applications, this data would typically come from a database.
# """

# # -------------------------------------
# # POST endpoint to add a new user
# # Validates input using UserInfo model
# # -------------------------------------
# @app.post("/adduser", status_code=status.HTTP_201_CREATED) # status_code=status.HTTP_201_CREATED this will be status response if /adduser got executed 
# def userdata(data: UserInfo):
#     """
#     This endpoint allows clients to add a new user.
#     It expects the request body to match the UserInfo Pydantic model.
#     The new user's data is appended to the in-memory `post_data` list.
#     """
#     post_data.append(data.dict())  # Converts the Pydantic object to a dictionary
#     return {"message": "User added successfully", "data": post_data}

# # -------------------------------------
# # GET endpoint to fetch all users
# # -------------------------------------
# @app.get("/usersinfo")
# def get_userinfo():
#     """
#     This endpoint returns all user data stored in `post_data`.
#     It sends the entire list of users as a response.
#     """
#     if len(post_data) != 0:
#         return {
#             "message": "Users info sent successfully",
#             "data": post_data
#         }
#     else:
#         raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="No users found in the list") 
#     #FastAPI builds the response normally but when it sees 204, it automatically removes the body before sending the response to the client.


# # -------------------------------------
# # Helper function to get the admin users
# # Filters users with admin_privileges set to True
# # -------------------------------------
# def get_admin_userinfo():
#     """
#     This helper function filters the users who have admin privileges set to True.
#     It checks the `admin_privileges` key in each user's data.
#     """
#     admin_users = []
#     for user in post_data:
#         if user.get("admin_privileges", False) == True:
#             admin_users.append(user)
#     return admin_users

# # -------------------------------------
# # GET endpoint to fetch all Admin users
# # -------------------------------------
# @app.get("/usersinfo/admin")
# def get_admin_users():
#     """
#     This endpoint returns a list of all users who have admin privileges.
#     It uses the `get_admin_userinfo` helper function to filter the users.
#     It also returns the total number of admin users and a list of their names.
#     """
#     admin_users = get_admin_userinfo()
#     return {
#         "message": "admin users info sent successfully",
#         "data": admin_users,
#         "total_admin_users": len(admin_users),
#         "list_of_admin_users": [user["name"] for user in admin_users]  # List of admin user names
#     }

# # -------------------------------------
# # Helper function to get the most recently added user
# # Note: Reverses the list temporarily
# # -------------------------------------
# def get_recent_user():
#     """
#     This helper function returns the most recently added user by reversing the `post_data` list.
#     It returns the first item after reversing the list.
#     Note: This function temporarily modifies the original list.
#     """
#     post_data.reverse()  # Modifies the list in place to reverse it
#     recent = post_data[0]
#     return recent

# # -------------------------------------
# # GET endpoint to fetch the most recent user
# # -------------------------------------
# @app.get("/usersinfo/recent_user")
# def get_recent_userinfo():
#     """
#     This endpoint returns the most recently added user.
#     It uses the `get_recent_user` helper function to retrieve the most recent user from the list.
#     """
#     Recent = get_recent_user()
#     return {
#         "message": "recent user info sent successfully",
#         "data": Recent
#     }

# # -------------------------------------
# # Helper function to filter users by place (case-insensitive)
# # -------------------------------------
# def userinfo_by_place(place):
#     """
#     This helper function filters users based on their place of residence.
#     It performs a case-insensitive comparison to find users living in the given place.
#     """
#     result = []
#     for p in post_data:
#         if p.get("place", "").lower() == place.lower():
#             result.append(p)
#     return result

# # -------------------------------------
# # GET endpoint to fetch users by place
# # URL format: /usersinfo/{place}
# # -------------------------------------
# @app.get("/usersinfo/{place}")
# def get_userinfo_by_place(place: str):
#     """
#     This endpoint returns a list of users who live in the specified place.
#     The `place` is passed as a path parameter, and the function filters users by their place of residence.
#     """
#     user_place = userinfo_by_place(place)
#     if not user_place:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No users found in {place}")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {"message": f"No users found in this {place}"}
#     # If no users are found, raise a 404 error with a custom message
#     # If users are found, return the list of users along with a success message

#     return {
#         "message": f"users info in {place} sent successfully",
#         "data": user_place
#     }
    
# # -------------------------------------
# # Delete endpoint to delete users by name
# # URL format: /usersinfo/delete/{name}
# # -------------------------------------    
# @app.delete("/usersinfo/delete/{name}")   
# def delete_userinfo(name :str):  # The 'name: str' type hint indicates that the 'name' parameter should be a string.if not it will thow an error
#     for user in post_data:
#         if user.get("name").lower() == name.lower():  # Correct method call
#             post_data.remove(user)  # Remove the user from the list
#             return {
#                 "message": f"user {name} was deleted from the list successfully",
#                 "data": post_data
#             }  
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user {name} was not found in list to delete")    

# # -------------------------------------
# # update endpoint to update users by name
# # URL format: /usersinfo/update/{name}
# # -------------------------------------    

# @app.put("/usersinfo/update/{name}")
# def update_userinfo(data: UserInfo, name: str):
#     """
#     This endpoint updates an existing user's information based on their name.
    
#     - If a user with the provided name exists (case-insensitive), their details are updated with the new data.
#     - If no user with the provided name is found, a new user is added to the list
#       and a 201 CREATED response is raised indicating a new user was added.
#     """
#     for user in post_data:
#         if user.get("name").lower() == name.lower():
#             user.update(data.dict())
#             return {"message": f"user {name}'s info updated"}

#     post_data.append(data.dict())
#     raise HTTPException(status_code=status.HTTP_201_CREATED, detail=f"new user {name}'s got added in the list")
