from fastapi import APIRouter,Depends
from app.utils.protectroute import get_current_user
from app.db.schemas.users import UserOutput

testrouter = APIRouter()


@testrouter.get("/me",response_model=UserOutput)
def get_me(current_user: UserOutput=Depends(get_current_user)):
    return current_user