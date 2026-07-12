from app.db.repository.base_repo import BaseRepository
from app.db.models.users import User
from app.db.models.sos import Sos

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
    
    def check_user_by_id(self,user_id:int):
        user = self.session.query(Sos).filter_by(user_id=user_id).first()
        return user

    def create_sos_event(self,create_sos:Sos):
        #  user = self.session.query(Sos).filter_by(user_id=create_sos.id)
        self.session.add(create_sos)
        self.session.commit()
        self.session.refresh(create_sos)
        return create_sos
         
    # def sos_info_send(self,user_id):
    #      pass
        

