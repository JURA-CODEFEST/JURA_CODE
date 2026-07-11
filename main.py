from fastapi import FastAPI  #, Depends
from contextlib import asynccontextmanager
from app.utils.init_db import create_tables
from app.router.auth import auth
from app.router.test import testrouter
from app.middleware.cors import usingcors
from app.router.refresh_sos_id import refresh_sos
# from app.utils.protectroute import get_current_user
# from app.db.schemas.users import UserOutput

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router=auth,tags=["auth"],prefix="/auth")
app.include_router(router=testrouter,tags=["test"],prefix="/test")
app.include_router(router=refresh_sos,tags=["sos"])

usingcors(app)

@app.get("/")
def index():
    return {"Home":"You are in home"}

