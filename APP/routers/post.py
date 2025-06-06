import APP.Oauth2
from fastapi import status, HTTPException ,Depends ,APIRouter # type: ignore
from APP.database import get_db
import APP.models
from sqlalchemy.orm import Session 
from APP.schema import post_data , Retrieve_data ,Retrieve_post_data_with_vote
from typing import List , Optional
from sqlalchemy import func


router = APIRouter(tags = ["Posts"])
# So I have experienced an issue like while getting the output of the API. thing is like it was due to response model. So I have created a new response model based on the original output and I have added a new response model to it. So it got rectified. 

@router.get("/Posts", response_model=List[Retrieve_post_data_with_vote]) #This line defines a GET endpoint at the path "/Posts" and specifies that the response will be a list of Retrieve_data objects.
def retrieve(db: Session = Depends(get_db),current_user: int = Depends(APP.Oauth2.get_current_user),limit: int = 10, skip: int = 0, Search: Optional[str] = ""): #You're injecting a APP.database session using FastAPI's Depends.
# # limit and skip are used for pagination are called query parameters in the context of FastAPI. and Search is an optional query parameter for filtering posts by name.

    # all_posts = db.query(APP.models.Post).filter(APP.models.Post.post_name.contains(Search)).limit(limit).offset(skip).all()  #This line queries the post table (from your APP.models module).   .all() fetches all rows as a list.
    all_posts = db.query(APP.models.Post, func.count(APP.models.vote.post_id).label("votes")).join(APP.models.vote, APP.models.vote.post_id == APP.models.Post.id, isouter=True).group_by(APP.models.Post.id).filter(APP.models.Post.post_name.contains(Search)).limit(limit).offset(skip).all()

    if len(all_posts) > 0:
        return all_posts
    else:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="No posts found") 


@router.get("/MyPosts", response_model=List[Retrieve_post_data_with_vote]) #
def retrieve(db: Session = Depends(get_db),current_user: int = Depends(APP.Oauth2.get_current_user)): #You're injecting a APP.database session using FastAPI's Depends.

    # all_posts = db.query(APP.models.Post).filter(APP.models.Post.owner_id == current_user.id).all()
  #This line queries the post table (from your APP.models module).   .all() fetches all rows as a list.
    all_posts = db.query(APP.models.Post, func.count(APP.models.vote.post_id).label("votes")).join(APP.models.vote, APP.models.vote.post_id == APP.models.Post.id, isouter=True).group_by(APP.models.Post.id).filter(APP.models.Post.owner_id == current_user.id).all()

    if len(all_posts) > 0:
        return all_posts
    else:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="No posts found") 


@router.post("/Posts/create", status_code=status.HTTP_201_CREATED,response_model=Retrieve_post_data_with_vote)
def create_new_post(post : post_data, db: Session = Depends(get_db),current_user: int = Depends(APP.Oauth2.get_current_user)):
                    #variable : #pyantic # db session using fastapi depends
    # new_post = APP.models.Post(post_name=post.post_name, description= post.description,published = post.published)
    # db.add(new_post) # Adding the new object to the session
    # db.commit() # Committing to the APP.database (actually saving the new post)
    # db.refresh(new_post)
    new_post = APP.models.Post(owner_id=current_user.id,**post.dict()) #When you want to create a new record (like a new post), you're not querying existing data—you're inserting a new entry. Hence, you don't need to use db.query() for creation.
    db.add(new_post)# Adding the new object to the session
    db.commit() # Committing to the APP.database (actually saving the new post)
    db.refresh(new_post) # Refreshing the object to get the latest info (like autogenerated fields)
    
    
    return new_post

# -------------------------------------
# GET endpoint to fetch all Published posts
# -------------------------------------
@router.get("/Posts/published",response_model=List[Retrieve_post_data_with_vote])
def get_published_Posts(db: Session = Depends(get_db),current_user: int = Depends(APP.Oauth2.get_current_user)):
    
    # post_Published = db.query(APP.models.Post).filter(APP.models.Post.published == True).all()
    post_Published = db.query(APP.models.Post, func.count(APP.models.vote.post_id).label("votes")).join(APP.models.vote, APP.models.vote.post_id == APP.models.Post.id, isouter=True).group_by(APP.models.Post.id).filter(APP.models.Post.published == True).all()


    
    if post_Published != 0:
        return post_Published 
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No posts Published yet") 
    
@router.get("/Posts/unpublished",response_model=list[Retrieve_post_data_with_vote])
def get_published_Posts(db: Session = Depends(get_db),current_user: int = Depends(APP.Oauth2.get_current_user)):
    
    # post_unPublished = db.query(APP.models.Post).filter(APP.models.Post.published == False).all()
    post_unPublished = db.query(APP.models.Post, func.count(APP.models.vote.post_id).label("votes")).join(APP.models.vote, APP.models.vote.post_id == APP.models.Post.id, isouter=True).group_by(APP.models.Post.id).filter(APP.models.Post.published == True).all()


    
    if post_unPublished != 0:
        return post_unPublished   
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No unPublished post presents")     
      
      

# # -------------------------------------
# # GET endpoint to fetch the most recent post
# # -------------------------------------
 
@router.get("/Posts/recent",response_model= Retrieve_post_data_with_vote)
def get_recent_userinfo( db: Session = Depends(get_db),current_user: int = Depends(APP.Oauth2.get_current_user)): 
    
    # recent_post = db.query(APP.models.Post).filter(APP.models.Post.published == True).order_by(APP.models.Post.created_at.desc()).first()
    recent_post= db.query(APP.models.Post, func.count(APP.models.vote.post_id).label("votes")).join(APP.models.vote, APP.models.vote.post_id == APP.models.Post.id, isouter=True).group_by(APP.models.Post.id).order_by(APP.models.Post.created_at.desc()).first()
    if recent_post is not None:
        return recent_post
        
        
    else:
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No posts Published yet") 
    

@router.get("/MyPosts/recent",response_model= Retrieve_post_data_with_vote)
def get_recent_userinfo( db: Session = Depends(get_db),current_user: int = Depends(APP.Oauth2.get_current_user)): 
    
    # myrecent_post = db.query(APP.models.Post).filter(APP.models.Post.published == True,APP.models.Post.owner_id == current_user.id).order_by(APP.models.Post.created_at.desc()).first()
    myrecent_post = db.query(APP.models.Post, func.count(APP.models.vote.post_id).label("votes")).join(APP.models.vote, APP.models.vote.post_id == APP.models.Post.id, isouter=True).group_by(APP.models.Post.id).filter(APP.models.Post.owner_id == current_user.id).order_by(APP.models.Post.created_at.desc()).first()
    
    if myrecent_post is not None:
       
        return myrecent_post
        
    else:
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No posts Published yet")     
    

      
@router.get("/Posts/{id}",response_model=Retrieve_post_data_with_vote)
def get_Post_by_id(id :int, db: Session = Depends(get_db),current_user: int = Depends(APP.Oauth2.get_current_user)):
    
    # Post_by_id = db.query(APP.models.Post).filter(APP.models.Post.id == id).first()
    Post_by_id = db.query(APP.models.Post, func.count(APP.models.vote.post_id).label("votes")).join(APP.models.vote, APP.models.vote.post_id == APP.models.Post.id, isouter=True).group_by(APP.models.Post.id).filter(APP.models.Post.id == id).first()

    
    
    if Post_by_id is not None:  #In Python, psycopg2's fetchone() method returns None when no row is found. So, checking for 0 doesn't work in this case because the default return value for no result is None, not 0.
        return Post_by_id
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Post find with id {id}")    
   
   

    
# # # -------------------------------------
# # # Delete endpoint to delete users by name
# # # URL format: /usersinfo/delete/{name}
# # # -------------------------------------

@router.delete("/Posts/delete/{id}", response_model=Retrieve_data)
def delete_Post(id: int, db: Session = Depends(get_db), current_user: APP.models.Users = Depends(APP.Oauth2.get_current_user)):

    # Query the post instance
    delete_post = db.query(APP.models.Post).filter(APP.models.Post.id == id).first()

    if delete_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {id} was not found in the list to delete"
        )

    # Check ownership
    if delete_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this post"
        )

    # Perform deletion
    db.delete(delete_post)
    db.commit()

    return delete_post
    


# # # -------------------------------------
# # # update endpoint to update users by id
# # # -------------------------------------    

@router.put("/Posts/update/{id}",response_model= Retrieve_data)
def update_Post(post: post_data, id: int, db: Session = Depends(get_db),current_user: int = Depends(APP.Oauth2.get_current_user)):
    
    post_query = db.query(APP.models.Post).filter(APP.models.Post.id == id) 
    # this post_query contain A query object, it is the object that SQLAlchemy generates when you construct a query, but you haven't executed it yet.


    new_post = post_query.first() # Adding methods to query objects like .first(),.all() will return the result immediately..

    if  new_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} was not found in list to update")
    
    if new_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not Authorized to Update the post")
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

# Converts the Pydantic object to a dictionary:post_data(title="New Title", content="Updated text")  post_data.dict ===> {'title': 'New Title', 'content': 'Updated text'}
# Translates to SQL: UPDATE posts SET title='New Title', content='Updated text' WHERE id=3
# synchronize_session=False skips syncing in-memory objects, improving performance
# db.commit() applies and saves the update permanently to the APP.database

    return  post_query.first() # this will fetch the newly updated post after saving   post_query.first()

# Explanationn
# post_query = db.query(APP.models.Post).filter(APP.models.Post.id == id)
# → This creates a SQLAlchemy query object to find a post with the given ID — but doesn’t execute it yet.

# post = post_query.first()
# → Executes the query to fetch the actual post from the APP.database and stores it in the post variable (an instance of the ORM model, not the Pydantic model).

# post_query.update(post_data.dict(), synchronize_session=False)
# → Updates the APP.database row with the new values provided in the request body (post_data, a Pydantic model), converting it to a dictionary with .dict().

# db.commit()
# → Permanently saves the updated values to the APP.database.    

