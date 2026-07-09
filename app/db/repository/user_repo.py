from app.db.repository.base_repo import BaseRepository
from app.db.models.users import User
from app.db.schemas.users import UserSignUp

class UserRepository(BaseRepository):
    def create_user(self,user_entered_data : UserSignUp):
        newUser = User(**user_entered_data.model_dump(exclude_none=True))
        self.session.add(instance = newUser)
        self.session.commit()
        self.session.refresh(instance = newUser)
        return newUser
    
    def check_user_by_email(self, user_entered_email:str)-> bool:
        user = self.session.query(User).filter_by(email=user_entered_email).first()
        return bool(user)
    
    def get_data_by_email(self,user_entered_email:str):
        user = self.session.query(User).filter_by(email=user_entered_email).first()
        return user
    
    def check_user_by_id(self, user_id: int):
        user = self.session.query(User).filter_by(id=user_id).first()
        return user