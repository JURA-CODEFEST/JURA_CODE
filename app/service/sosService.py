from app.core.security.api_generator import API_generator
from sqlalchemy.orm import Session
from app.db.repository.sos_repo import SosRepo
from app.db.repository.user_repo import UserRepository


class SosService:
        def __init__(self,session: Session):
            self.__userRepo = UserRepository(session=session)
            self.__sosRepo = SosRepo(session = session)
            
        def refresh_sosid(self,user_id:int):
            if self.__userRepo.check_user_by_id(user_id=user_id):
                while True:
                    new_api = API_generator.generate_secure_string(16)
                    user = self.__sosRepo.check_user_by_sos_id(new_api)
                    if not user:
                        self.__sosRepo.update_sos_id(user_id,new_api)
                        return {"new_sos_id":new_api}