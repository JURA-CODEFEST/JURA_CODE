from fastapi import APIRouter,Depends
from app.core.database import get_db
from sqlalchemy.orm import Session

guardian = APIRouter

@guardian.get("/guardian/list")
def listguardian(session : Session=Depends(get_db)):
    pass