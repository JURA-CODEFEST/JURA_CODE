from app.service.userService import UserService
from app.db.schemas.users import UserToken,UserLogin,UserOutput,UserSignUp
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends
from app.core.database import get_db

auth = APIRouter()

@auth.post("/login",status_code=200,response_model=UserToken)
def login(LoginDetails: UserLogin, session : Session=Depends(get_db)):
    try:
        return UserService(session=session).login(userdetails=LoginDetails)
    except Exception as error:
        print(error)
        raise error
    

@auth.post("/signup",status_code=200,response_model=UserOutput)
def signup(SignupDetails: UserSignUp, session:Session=Depends(get_db)):
    try:
        return UserService(session=session).signup(userdetails=SignupDetails)
    except Exception as error:
        print(error)
        raise error