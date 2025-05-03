
from pydantic import BaseModel  # type: ignore
# -------------------------------------
# Pydantic model to validate user input
# -------------------------------------
PYDANTIC_MODEL = BaseModel
class post_data(PYDANTIC_MODEL):
    """
    Pydantic model to define the structure of user data.
    This ensures that the data coming to the API is validated and properly formatted.
    """
    post_name: str
    description: str
    published: bool

class retrive_data(post_data):
    """
    Pydantic model to define the structure of user data.
    This ensures that the data coming to the API is validated and properly formatted.
    """
    id: int
     
    class Config:
        orm_mode = True    
    