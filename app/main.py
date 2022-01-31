from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models
from app.config import settings
from app.database import engine
from app.routers import post, user, auth, vote

# This makes sqlalchemy to create the database tables not needed as we have alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]  # This means all domains can access our API

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# So FASTAPI can get the routes defined in routers files
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Welcome to my application pushed to heroku by ci/cd"}
