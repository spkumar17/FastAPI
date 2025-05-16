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

    user = db.query(APP.models.Users).filter(APP.models.Users.id == token.id).first()

    return user


def verify_access_token(token: token,credentials_exception):  # token is from 
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        
        if id is None:
            raise credentials_exception
        token_data = tokendata(id=id) # from APP.schema
        
    except JWTError:
        raise credentials_exception
    
    return token_data
