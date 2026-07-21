from app.db.repository.user_repo import UserRepository
from app.core.security.authHandler import AuthHandler
from app.core.security.hashHandler import HashHelper
from app.core.security.api_generator import API_generator
from sqlalchemy.orm import Session
from app.db.schemas.users import UserSignUp,UserLogin,UserToken
from app.db.models.users import User
from fastapi import HTTPException
from app.core.security.otp_generator import OTPgenerator
from datetime import datetime,timedelta 
from app.db.repository.otp_repo import OTPrepository
from app.db.models.register_otp import OTPRegister
from app.utils.mail_sender import verify_email
from app.utils.mail_sender import forget_password as fp
from pydantic import EmailStr


class UserService:
    def __init__(self,session: Session):
        self.__userRepo = UserRepository(session = session)
        self.__otpRepo = OTPrepository(session = session)
        self.session = session


    async def signup(self,userdetails:UserSignUp):
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
            sos_id = api,
            verified = False
        )

        new_user_create = self.__userRepo.create_user(new_user)
        otp_gen = OTPgenerator.generate_numeric_otp()
        expires_at = datetime.utcnow()+timedelta(minutes=10)


        otp_table = OTPRegister(
            user_id = new_user_create.id,
            email = new_user_create.email,
            otp = otp_gen,
            expires_at = expires_at
        )
        self.__otpRepo.create_otp(otp_table)

        self.session.commit()

        await verify_email([otp_table.email],otp_table.otp)

        return {"message":"Email has been sent Successfully"}
        
    async def resend_otp(self,email):
        user = self.__userRepo.get_data_by_email(user_entered_email=email)

        if not user:
            raise HTTPException(status_code=400,detail="Register First")
        otp_data = self.__otpRepo.get_otp(email=email)

        if not otp_data:
            raise HTTPException(status_code=400,detail="No otp data for this")
        
        if user.verified:
            raise HTTPException(status_code=400,detail="Already verified this email")
        otp_gen = OTPgenerator.generate_numeric_otp()
        expires = datetime.utcnow()+timedelta(minutes=10)

        otp_data.otp = otp_gen
        otp_data.expires_at = expires
        self.__otpRepo.update_otp(otp_data)
        self.session.commit()
        await verify_email([email],otp_gen)
        return {"message":"The otp has been resent"}


    def verify_email(self,email:EmailStr,otp:int):
        user = self.__userRepo.get_data_by_email(user_entered_email=email)
        if not user:
            raise HTTPException(status_code=400,detail="User not found")
        
        if user.verified:
            raise HTTPException(status_code=400,detail="User already verified")
        
        otp_data_for_user = self.__otpRepo.get_otp(email=email)
        if not otp_data_for_user:
            raise HTTPException(status_code=400,detail="Otp detail not found")

        if (otp_data_for_user.expires_at <datetime.utcnow()):
            raise HTTPException(status_code=400,detail="Otp expired")
        

        if otp_data_for_user.otp==otp:
            user.verified=True
            self.__userRepo.update_user(user=user)
            self.__otpRepo.delete_otp(email=email)
            self.session.commit()

            return {"message":"User has been verified"}

        raise HTTPException(status_code=400,detail="OTP not valid")
        

    def login(self,userdetails:UserLogin):
        if not self.__userRepo.check_user_by_email(user_entered_email=userdetails.email):
            raise HTTPException(status_code=400,detail="Email not found")
        

        user = self.__userRepo.get_data_by_email(user_entered_email=userdetails.email)
        if not user.verified:
            raise HTTPException(status_code=400,detail="Email Not verified")
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
    


    async def forget_password(self,email:EmailStr):
        user = self.__userRepo.get_data_by_email(user_entered_email=email)
        if not user:
            raise HTTPException(status_code=400,detail="No user with such email")
        if not user.verified:
            raise HTTPException(status_code=400,detail="Please verify your email first")
        
        otp_data = self.__otpRepo.get_otp(email=email)
        if otp_data:
            self.__otpRepo.delete_otp(email=email)

        
        otp = OTPgenerator.generate_numeric_otp()
        expires = datetime.utcnow()+timedelta(minutes=10)
        
        otp_table = OTPRegister(
            user_id= user.id,
            email = user.email,
            otp = otp,
            expires_at = expires

        )
        self.__otpRepo.create_otp(otp_table)
        self.session.commit()
        await fp([email],otp=otp)
        return {"message":"email sent"}
    
    def change_password(self,email:EmailStr,otp:int,password:str):
        user = self.__userRepo.get_data_by_email(user_entered_email=email)
        if not user:
            raise HTTPException(status_code=400,detail="User not found")
        
        if not user.verified:
            raise HTTPException(status_code=400,detail="User not verified")
        
        # if user.verified:
        #     raise HTTPException(status_code=400,detail="User already verified")
        
        otp_data_for_user = self.__otpRepo.get_otp(email=email)
        if not otp_data_for_user:
            raise HTTPException(status_code=400,detail="Otp detail not found")

        if (otp_data_for_user.expires_at <datetime.utcnow()):
            raise HTTPException(status_code=400,detail="Otp expired")
        

        if otp_data_for_user.otp==otp:
            hashedpassword = HashHelper.gethashed(plain_password=password)
            user.password = hashedpassword
            self.__userRepo.update_user(user=user)
            self.__otpRepo.delete_otp(email=email)
            self.session.commit()

            return {"message":"Password Changed"}

        raise HTTPException(status_code=400,detail="OTP not valid")
        


    
    # def refresh_sosid(self,user_id:int):
    #     if self.__userRepo.check_user_by_id(user_id=user_id):
    #         while True:
    #             new_api = API_generator.generate_secure_string(16)
    #             user = self.__userRepo.check_user_by_sos_id(new_api)
    #             if not user:
    #                 self.__userRepo.update_sos_id(user_id,new_api)
    #                 return {"new_sos_id":new_api}
                    
            
    #     raise HTTPException(status_code=400,detail="User not found")