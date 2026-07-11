from app.db.repository.base_repo import BaseRepository
from app.db.models.users import User

class SosRepo(BaseRepository):
    def update_sos_id(self,user_id:int,sos_id):
            user = self.session.query(User).filter_by(id=user_id).first()
            user.sos_id = sos_id
            self.session.commit()
            self.session.refresh(user)
            return user
    
    def check_user_by_sos_id(self,sos_id:str):
        user = self.session.query(User).filter_by(sos_id=sos_id).first()
        return user

