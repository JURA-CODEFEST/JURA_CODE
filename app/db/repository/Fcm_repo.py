from app.db.repository.base_repo import BaseRepository
from app.db.models.user_device_fcm import UserDeviceFCM

class FCMrepository(BaseRepository):
    def create_fcm(self,userdevice:UserDeviceFCM):
        self.session.add(userdevice)
        self.session.commit()
        self.session.refresh(userdevice)
        return userdevice
    
    def get_by_fcm(self,fcm_token):
        device = self.session.query(UserDeviceFCM).filter_by(fcm_token=fcm_token).first()
        return device

    def get_by_id(self,user_id):
        user = self.session.query(UserDeviceFCM).filter_by(user_id=user_id).all()
        return user


    def update_fcm(self,fcm_token,user_id):
        data = self.session.query(UserDeviceFCM).filter_by(fcm_token=fcm_token).first()
        data.user_id = user_id
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
