from fastapi import FastAPI # type: ignore
from APP.database import engine
import APP.models
from APP.routers import post, users, auth ,vote

from fastapi.middleware.cors import CORSMiddleware

APP.models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [ "*" ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def main_func():
    return "this is my first FastAPI Project"