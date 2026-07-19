from app.db.repository.user_repo import UserRepository
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.repository.Fcm_repo import FCMrepository
from app.db.models.user_device_fcm import UserDeviceFCM

class FcmService():
    def __init__(self,session: Session):
            self.__userRepo = UserRepository(session=session)
            self.__fcmRepo = FCMrepository(session=session)

    def save_fcm(self,user_id,fcm_token):
        user = self.__userRepo.check_user_by_id(user_id=user_id)
        if not user:
            raise HTTPException(status_code=400,detail="User not found")
        
        existing = self.__fcmRepo.get_by_fcm(fcm_token=fcm_token)
        if existing:
            if existing.user_id == user_id:
                 return existing
            existing.user_id = user_id
            return self.__fcmRepo.update_fcm(fcm_token=fcm_token,user_id=user_id)

        data = UserDeviceFCM(
             user_id = user_id,
             fcm_token = fcm_token
        )
        return self.__fcmRepo.create_fcm(data)
