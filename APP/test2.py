# # connecting to database using psycopg2
# from fastapi import FastAPI, Response, status, HTTPException  # type: ignore
# from fastapi.params import Body  # type: ignore # type: ignore Body(...) tells FastAPI to expect this value in the request body, not as a query or path parameter.
# from pydantic import BaseModel  # type: ignore
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# app = FastAPI()


# while True:
#     try:
#         # Connect to your PostgreSQL database
#         conn = psycopg2.connect(
#             dbname="FastAPI",  
#             user="postgres",   
#             password="Cloud@123",  
#             host="localhost",    
#             port="5432",         
#             cursor_factory=RealDictCursor  # Use RealDictCursor for dict-like results
#         ) #This is an optional argument. By specifying RealDictCursor, the cursor will return query results as dictionaries, with column names as keys. This makes the data more accessible compared to returning data as tuples.
#         cur = conn.cursor()
#         print("Database connection successful")
#         break  # Exit the loop if connection is successful
#     except Exception as error:
#         print("Database connection failed")
#         print("Error:", error)
#         time.sleep(5)  # Wait 5 seconds before retrying (not 50!)

        


# # -------------------------------------
# # Pydantic model to validate user input
# # -------------------------------------
# PYDANTIC_MODEL = BaseModel
# class post_data(PYDANTIC_MODEL):
#     """
#     Pydantic model to define the structure of user data.
#     This ensures that the data coming to the API is validated and properly formatted.
#     """
#     post_name: str
#     description: str
#     published: bool
    
    

# # -------------------------------------
# # GET endpoint to fetch posts
# # -------------------------------------
# @app.get("/Posts")
# def get_userinfo():
#     cur.execute(""" SELECT * FROM Posts;""")
#     post_data = cur.fetchall()
    
#     if len(post_data) != 0:
#         return {
#             "message": "data sent successfully",
#             "data": post_data
#         }
#     else:
#         raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="No users found in the list") 
#     #FastAPI builds the response normally but when it sees 204, it automatically removes the body before sending the response to the client.

# # -------------------------------------
# # GET endpoint to fetch all Published posts
# # -------------------------------------
# @app.get("/Posts/published")
# def get_published_Posts():
    
#     cur.execute(""" SELECT * FROM Posts WHERE published IS true;""")
#     post_Published = cur.fetchall()
    
#     if post_Published != 0:
#         return {
#             "message": "Published posts fetched successfully",
#             "data": post_Published,
#         }
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No posts Published yet") 
  


# # -------------------------------------
# # GET endpoint to fetch the most recent post
# # -------------------------------------
# @app.get("/Posts/recent")
# def get_recent_userinfo(): 
#     cur.execute(""" SELECT * FROM Posts WHERE published IS true ORDER BY created_at DESC LIMIT 1 ;""")
#     Recent = cur.fetchall()
    
#     if Recent !=0:
#         return {
#             "message": "recent POST info sent successfully",
#             "data": Recent
#         }
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No posts Published yet") 

            

# # -------------------------------------
# # GET endpoint to fetch Post by id
# # 
# # -------------------------------------
# @app.get("/Posts/{id}")
# def get_Post_by_id(id :int):
#     cur.execute(""" SELECT * FROM Posts WHERE id = %s ;""",(str(id),))
#     Post_by_id = cur.fetchone()
    
#     if Post_by_id is not None:  #In Python, psycopg2's fetchone() method returns None when no row is found. So, checking for 0 doesn't work in this case because the default return value for no result is None, not 0.
#         return {
#             "message": f"Post with id {id} sent successfully",
#             "data": Post_by_id
#             }
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Post find with id {id}")    
    

    
# # # -------------------------------------
# # # post endpoint to create post 
# # #
# # # ------------------------------------- 
   
# @app.post("/Posts/Create", status_code=status.HTTP_201_CREATED)   
# def create_new_post(post: post_data):
#     cur.execute("""INSERT INTO Posts (Post_name, Description, published) VALUES (%s, %s, %s) RETURNING *; """, (post.post_name, post.description, post.published))
#     Post_by_id = cur.fetchone()
#     conn.commit() 
#     return { "Message: View the created post"
#             "Data": Post_by_id
#         }
    
    

    
# # # -------------------------------------
# # # Delete endpoint to delete users by name
# # # URL format: /usersinfo/delete/{name}
# # # -------------------------------------    
# @app.delete("/Posts/delete/{id}")   
# def delete_Post(id : int):  # The 'name: str' type hint indicates that the 'name' parameter should be a string.if not it will thow an error
#     cur.execute("""DELETE FROM Posts WHERE id =%s RETURNING *; """,(str(id),))
#     Post_deleted_by_id = cur.fetchone()
#     conn.commit() 
#     if Post_deleted_by_id is not None:
            
#             return {
#                 "message": f"Post with id {id} was deleted from the list successfully",
#                 "data": Post_deleted_by_id
#             }  
#     else:        
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} was not found in list to delete")    

# # # -------------------------------------
# # # update endpoint to update users by id
# # # -------------------------------------    

# @app.put("/Posts/update/{id}")
# def update_Post(post: post_data, id: int):
#     cur.execute("""UPDATE Posts SET Post_name = %s, Description = %s, published = %s WHERE id = %s RETURNING *;""", (post.post_name, post.description, post.published, str(id)))    
#     Post_updated_by_id = cur.fetchone()
#     conn.commit() 
#     if Post_updated_by_id is not None:
#         return {"message": f"Post {id}'s info updated",
#                 "data": Post_updated_by_id 
#                 }
    
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} was not found in list to update")
