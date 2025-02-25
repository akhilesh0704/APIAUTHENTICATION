from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from app.util.init_db import create_tables
from app.routers.auth import authRouter
from app.util.protectRoute import get_current_user
from app.db.schema.user import UserOutput

@asynccontextmanager
async def lifespan(app:FastAPI):
    #INITIALIZE DB AT START
    print("Created")
    create_tables()
    yield #separation point

app = FastAPI(lifespan=lifespan)
app.include_router(router=authRouter, tags=["auth"], prefix="/auth")
# /auth/login
#/auth/signup


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

@app.get("/health")
def health_check():
    return {"status": "Running..."}

@app.get("/protected")
def read_protected(user: UserOutput = Depends(get_current_user)):
    return {"data" : user}
