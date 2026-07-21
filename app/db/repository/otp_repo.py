from app.db.repository.base_repo import BaseRepository
from app.db.models.register_otp import OTPRegister


class OTPrepository(BaseRepository):
    def create_otp(self,otp:OTPRegister):
        self.session.add(otp)
        self.session.flush()
        self.session.refresh(otp)
        return otp


    def get_otp(self,email):
        data = self.session.query(OTPRegister).filter_by(email=email).first()
        return data
    

    def update_otp(self,otp:OTPRegister):
        self.session.add(otp)
        self.session.flush()
        self.session.refresh(otp)
        return otp
    
    def delete_otp(self,email):
        return self.session.query(OTPRegister).filter_by(email=email).delete()