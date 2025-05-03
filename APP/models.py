from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP,func
from database import Base


# declarative_base() is an inbuilt function from SQLAlchemy.
# It creates a base class (usually named Base).
# Any class (like Post) that inherits from Base will be mapped to a database table.
# So when you write the Post class and inherit Base, SQLAlchemy knows:
# ➔ "Okay, I need to create a posts table in the database."
# Base gives power to Post class to become a real table in the database.


class Post(Base):
    __tablename__ = "posts" # Table name
    id = Column(Integer, primary_key = True, nullable = False,autoincrement=True)
    post_name = Column(String, nullable = False)
    description  = Column(String, nullable = False)
    published = Column(Boolean, default = True, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())


class Users(Base):
    __tablename__ = "users" # Table name
    id = Column(Integer, primary_key = True, nullable = False,autoincrement=True)
    user_name = Column(String, nullable = False)
    email_id = Column(String, nullable = False,unique = True)
    password   = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
