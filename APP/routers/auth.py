from fastapi import status, HTTPException ,Depends , APIRouter # type: ignore
from database import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import models 
from sqlalchemy.orm import Session
import utils
import Oauth2


router = APIRouter(tags = ["Authentication"])


@router.post("/login")
def create_new_post(User_Credentials : OAuth2PasswordRequestForm = Depends() , db: Session = Depends(get_db)):
    # if we use OAuth2PasswordRequestForm we no longer need to send the data in body instead it will use a form with username and password
    # email_id will be called as username 
    # password 
    user_verify = db.query(models.Users).filter(models.Users.email_id == User_Credentials.username).first()
    
    if user_verify  is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Credentials") 
    
    verify_password = utils.verify(User_Credentials.password,user_verify.password )
    
    if not verify_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Credentials") 
    
    token = Oauth2.create_access_token({"user_id": user_verify.id })

    return {"access_token": token, "token_type": "bearer"}
