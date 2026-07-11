from app.db.repository.user_repo import UserRepository
from app.core.security.authHandler import AuthHandler
from app.core.security.hashHandler import HashHelper
from app.core.security.api_generator import API_generator
from sqlalchemy.orm import Session
from app.db.schemas.users import UserSignUp,UserLogin,UserToken
from app.db.models.users import User
from fastapi import HTTPException


class UserService:
    def __init__(self,session: Session):
        self.__userRepo = UserRepository(session = session)


    def signup(self,userdetails:UserSignUp):
        if self.__userRepo.check_user_by_email(user_entered_email=userdetails.email):
            raise HTTPException(status_code=400, detail="Email already exists")
        
        hashedpassword = HashHelper.gethashed(plain_password=userdetails.password)
        api = API_generator.generate_secure_string(16)
        # userdetails.password = hashedpassword
        new_user = User(
            first_name = userdetails.first_name,
            last_name = userdetails.last_name,
            email = userdetails.email,
            password = hashedpassword,
            sos_id = api
        )
        
        return self.__userRepo.create_user(new_user)


    def login(self,userdetails:UserLogin):
        if not self.__userRepo.check_user_by_email(user_entered_email=userdetails.email):
            raise HTTPException(status_code=400,detail="Email not found")
        
        user = self.__userRepo.get_data_by_email(user_entered_email=userdetails.email)
        if HashHelper.verifyhashedpassword(plain_password=userdetails.password,hashed_password=user.password):
            token = AuthHandler.signjwt(user_id=user.id)
            if token:
                return UserToken(token=token)
            raise HTTPException(status_code=500,detail="Couldnot handle request. Please try again")
        raise HTTPException(status_code=400,detail = "Wrong Credentials")
    
    def get_user_by_id(self,user_id:int):
        user = self.__userRepo.check_user_by_id(user_id=user_id)
        if user:
            return user
        raise HTTPException(status_code=400,detail="User not found")
    
    def refresh_sosid(self,user_id:int):
        if self.__userRepo.check_user_by_id(user_id=user_id):
            while True:
                new_api = API_generator.generate_secure_string(16)
                user = self.__userRepo.check_user_by_sos_id(new_api)
                if not user:
                    self.__userRepo.update_sos_id(user_id,new_api)
                    return {"new_sos_id":new_api}
                    
            
        raise HTTPException(status_code=400,detail="User not found")