
from fastapi import status, HTTPException ,Depends , APIRouter # type: ignore
from APP.database import get_db
import APP.models
from sqlalchemy.orm import Session
import APP.schema
import APP.Oauth2

router = APIRouter(tags = ["Votes"])

@router.post("/Vote", status_code=status.HTTP_201_CREATED)
def vote_post( vote : APP.schema.vote, db: Session = Depends(get_db),current_user: int = Depends(APP.Oauth2.get_current_user)):
    
    post_query = db.query(APP.models.Post).filter(APP.models.Post.id == vote.post_id)
    post_found = post_query.first()
    if not post_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} not found")
    
    vote_query = db.query(APP.models.vote).filter(APP.models.vote.post_id == vote.post_id, APP.models.vote.user_id == current_user.id)
    found_vote = vote_query.first()
    
    if vote.direction == 1:
        
        if found_vote :
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have already voted for this post")
        # if the user has already voted for the post, we will not allow them to vote again
        # we will raise a conflict error   
        else:
            add_vote = APP.models.vote(post_id = vote.post_id, user_id = current_user.id)
            db.add(add_vote)
            db.commit()
            db.refresh(add_vote)
            return {"message": "Vote added successfully"}     
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found")
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message": "Vote deleted successfully"}
     