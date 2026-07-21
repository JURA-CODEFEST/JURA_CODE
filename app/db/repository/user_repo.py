from app.db.repository.base_repo import BaseRepository
from app.db.models.users import User
# from app.db.schemas.users import UserSignUp

class UserRepository(BaseRepository):
    def create_user(self,user : User):
        # newUser = User(**user_entered_data.model_dump(exclude_none=True))
        self.session.add(user)
        self.session.flush()
        self.session.refresh(user)
        return user
    
    def check_user_by_email(self, user_entered_email:str)-> bool:
        user = self.session.query(User).filter_by(email=user_entered_email).first()
        return bool(user)
    
    def get_data_by_email(self,user_entered_email:str):
        user = self.session.query(User).filter_by(email=user_entered_email).first()
        return user
    
    def check_user_by_id(self, user_id: int):
        user = self.session.query(User).filter_by(id=user_id).first()
        return user
    
    def update_user(self,user:User):
        self.session.add(user)
        self.session.flush()
        self.session.refresh(user)
        return user
    
    # def update_sos_id(self,user_id:int,sos_id):
    #     user = self.session.query(User).filter_by(id=user_id).first()
    #     user.sos_id = sos_id
    #     self.session.commit()
    #     self.session.refresh(user)
    #     return user
    
    # def check_user_by_sos_id(self,sos_id:str):
    #     user = self.session.query(User).filter_by(sos_id=sos_id).first()
    #     return user
    