from fastapi import FastAPI, status, HTTPException ,Depends , APIRouter # type: ignore
from database import get_db
import models
from sqlalchemy.orm import Session
from schema import Users_cred
import utils


router = APIRouter(tags = ["Authentication"])


@router.post("/login")
def create_new_post(User_Credentials : Users_cred , db: Session = Depends(get_db)):
    
    user_verify = db.query(models.users).filter(models.users.email_id == User_Credentials.email_id).first()
    
    if user_verify  is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials") 
    
    verify_password = utils.verify(User_Credentials.password,user_verify.password )
    
    if not verify_password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials") 
    
    return {"verify":"successfully logged in"}

        
    

        
        
    
    