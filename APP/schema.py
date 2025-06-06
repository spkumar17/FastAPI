
from datetime import datetime
from pydantic import BaseModel,EmailStr # type: ignore
from typing import Annotated
from pydantic import Field

# -------------------------------------
# Pydantic model to validate user input
# -------------------------------------
PYDANTIC_MODEL = BaseModel

class Users_data(PYDANTIC_MODEL):
    """
    Pydantic model to define the structure of data.
    This ensures that the data coming to the API is validated and properly formatted.
    """
    user_name: str
    email_id: EmailStr
    password:str

    
class Retrieve_userdata(PYDANTIC_MODEL):
    """
    Pydantic model to define the structure of data.
    This ensures that the data comming out from API is in desired formatted.
    """
    id: int
    user_name: str
    email_id: EmailStr
    created_at: datetime

     
    class Config:
        orm_mode = True     
        
class post_data(PYDANTIC_MODEL):
    """
    Pydantic model to define the structure of data.
    This ensures that the data coming to the API is validated and properly formatted.
    """
    post_name: str
    description: str
    published: bool

class Retrieve_data(post_data):
    """
    Pydantic model to define the structure of data.
    This ensures that the data comming out from API is in desired formatted.
    """
    id: int
    created_at: datetime
    owner : Retrieve_userdata # instance of Retrieve_userdata(inhertied this from retrive_userdata)
    
    class Config:
        orm_mode = True    
    
class Retrieve_post_data_with_vote(PYDANTIC_MODEL):  # 
    """So like recently I have experienced an issue like while getting the output of the API. 
    One thing is like it was due to response model. So I have created a new response model based on the original output 
    and I have added a new response model to it. So it got rectified. 

    """
    Post :Retrieve_data # instance of Retrieve_data(inhertied this from retrive_data)
    votes: int
    
    class Config:
        orm_mode = True
        
# #-------------------------------------
# 
#     {
#         "Post": {
#             "post_name": "first",
#             "description": "ds",
#             "published": true,
#             "id": 2,
#             "created_at": "2025-05-08T16:51:50.187093+05:30",
#             "owner": {
#                 "id": 5,
#                 "user_name": "Kumar",
#                 "email_id": "Kumar@gmail.com",
#                 "created_at": "2025-05-07T14:31:40.375086+05:30"
#             }
#         },
#         "votes": 1
#     },
#     -----------------------        
class Users_cred(PYDANTIC_MODEL):
    
    email_id: EmailStr
    password:str

class token(PYDANTIC_MODEL):
    access_token: str
    access_type: str 

class tokendata(PYDANTIC_MODEL):
    id : int    
    
    
class vote(PYDANTIC_MODEL):
    post_id: int
    direction: Annotated[int, Field(le=1)]    