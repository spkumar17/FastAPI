from jose import JWTError , jwt
from APP.schema import token,tokendata
from datetime import datetime,timedelta
from fastapi import status, HTTPException ,Depends# type: ignore
from APP.database import get_db
from sqlalchemy.orm import Session
import APP.models 
from APP.config import settings
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# "The line oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login') in FastAPI defines a security dependency that extracts a bearer token from the Authorization header of incoming HTTP requests. It’s part of how FastAPI implements OAuth2 password flow for authentication.
# The tokenUrl='login' parameter specifies the URL endpoint where clients can obtain the token, which is mainly used for automatic API documentation like Swagger UI.
# This dependency doesn’t validate the token itself; it only retrieves it. The actual token validation and user authentication need to be handled separately, typically by decoding and verifying the JWT token inside the endpoint or a dedicated authentication function."



# SECRET_KEY 
# ALGORITHM
# ACCESS_TOKEN_EXPIRE_MINUTES
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    # if verify_access_token is valid the it return the token_data.id 
    # token = token_data.id ====> token.id = token_data.id
    # this token.id will return the user id which is extracted from the token.

    user = db.query(APP.models.Users).filter(APP.models.Users.id == token.id).first()

    return user


def verify_access_token(token: token,credentials_exception):  # token is from APP.schema
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        
        if id is None:   # To validate the token and extract the user’s ID from it, so we can later fetch the correct user from the database.
            raise credentials_exception
        token_data = tokendata(id=id) # from APP.schema
        # You’re creating an object of the tokendata class and initializing it with id.
        # Pydantic will validate that id(7) is indeed an int (as defined).
        # it will return token_data.id  # gives you 7

    except JWTError:
        raise credentials_exception   # If validation fails (jwt.decode fails) , you'll get the credentials_exception error.


    
    return token_data
