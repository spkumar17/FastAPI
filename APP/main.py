from fastapi import FastAPI # type: ignore
from database import engine
import models
from routers import post, users, auth

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
def main_func():
    return "this is my first FastAPI Project"