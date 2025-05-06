from jose import JWTError , jwt
from schema import token,tokendata
from datetime import datetime,timedelta
from fastapi import status, HTTPException ,Depends ,Session# type: ignore
from fastapi.security import OAuth2PasswordBearer
from database import get_db
import models 


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


# SECRET_KEY 
# ALGORITHM
# ACCESS_TOKEN_EXPIRE_MINUTES
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.Users).filter(models.Users.id == token.id).first()

    return user


def verify_access_token(token: token,credentials_exception):  # token is from 
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        
        if id is None:
            raise credentials_exception
        token_data = tokendata(id=id) # from schema
        
    except JWTError:
        raise credentials_exception
    
    return token_data
