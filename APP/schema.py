
from datetime import datetime
from pydantic import BaseModel,EmailStr  # type: ignore
# -------------------------------------
# Pydantic model to validate user input
# -------------------------------------
PYDANTIC_MODEL = BaseModel
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
     
    class Config:
        orm_mode = True    
    

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
        

# class Users_cred(PYDANTIC_MODEL):
#     """
#     Pydantic model to define the structure of data.
#     This ensures that the data coming to the API is validated and properly formatted.
#     """
#     email_id: EmailStr
#     password:str

            