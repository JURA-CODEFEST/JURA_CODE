from app.service.userService import UserService
from app.db.schemas.users import UserToken,UserLogin,UserSignUp,User_first_signup
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends
from app.core.database import get_db
from pydantic import EmailStr

auth = APIRouter()

@auth.post("/login",status_code=200,response_model=UserToken)
def login(LoginDetails: UserLogin, session : Session=Depends(get_db)):
    try:
        return UserService(session=session).login(userdetails=LoginDetails)
    except Exception as error:
        print(error)
        raise error
    

@auth.post("/signup",status_code=200,response_model=User_first_signup)
async def signup(SignupDetails: UserSignUp, session:Session=Depends(get_db)):
    try:
        return await UserService(session=session).signup(userdetails=SignupDetails)
    except Exception as error:
        print(error)
        raise error
    
@auth.post("/resend-otp")
async def resend_otp(email:EmailStr,session:Session=Depends(get_db)):
    try:
        return await UserService(session=session).resend_otp(email=email)
    except Exception as error:
        print(error)
        raise error
    
@auth.post("/otp-verify")
def verify_email(email:EmailStr,otp:int,session:Session=Depends(get_db)):
    try:
        return  UserService(session=session).verify_email(email=email,otp=otp)
    except Exception as error:
        print(error)
        raise error
    
@auth.post("/forget-password")
async def forget_password(email:EmailStr,session:Session=Depends(get_db)):
    try:
        return await UserService(session=session).forget_password(email=email)
    except Exception as error:
        print(error)
        raise error
    
@auth.post("/change-password")
def change_password(email:EmailStr,otp:int,password:str,session:Session=Depends(get_db)):
    try:
        return UserService(session=session).change_password(email=email,otp=otp,password=password)
    except Exception as error:
        print(error)
        raise error