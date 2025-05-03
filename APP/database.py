from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2  

# SQLAlchemy needs a database driver to talk to PostgreSQL.
# By default, SQLAlchemy does not include a PostgreSQL driver — you need to install one separately.
# The most commonly used PostgreSQL driver is:
# psycopg2 (or the lightweight version: psycopg2-binary)
from psycopg2.extras import RealDictCursor
import time

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Cloud%40123@localhost:5432/FastAPI'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
# This creates a connection to your PostgreSQL server.
# engine is used internally by SQLAlchemy ORM to talk to your database.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# This creates database sessions.
# Session = A temporary connection to run SQL queries.
# autocommit=False means: You need to manually commit changes (good for control).
# autoflush=False means: It won't automatically flush changes to database until you ask.

Base = declarative_base()
# Base is the starting point for your ORM models (like Post, User, etc.).
# Every model should inherit from this Base.
# Mapping classes to database tables
# Enabling ORM features (querying, inserting, updating, deleting without SQL)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
# FastAPI-Project/
# │
# ├── app/
# │   ├── __init__.py
# │   ├── main.py          # FastAPI app starts here
# │   ├── models.py        # SQLAlchemy models (Post, User etc.)
# │   ├── schemas.py       # Pydantic models (Request & Response validation)
# │   ├── database.py      # DB connection and Base
# │   ├── crud.py          # Database operation functions (create, read, update, delete)
# │   ├── routers/
# │   │   ├── __init__.py
# │   │   ├── post.py      # Routes related to Posts
# │   │   └── user.py      # Routes related to Users
# │   └── utils/
# │       ├── __init__.py
# │       └── helper.py    # Helper functions (eg., hashing password, JWT tokens)
# │
# ├── alembic/             # (Optional) For database migrations
# ├── requirements.txt     # All dependencies
# ├── README.md            # Project description
# └── .env                 # Environment variables (DB URL, secrets, etc.)
        

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