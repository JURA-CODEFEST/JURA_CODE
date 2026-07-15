from app.core.security.api_generator import API_generator
from sqlalchemy.orm import Session
from app.db.repository.sos_repo import SosRepo
from app.db.repository.guardian_repo import GuardianRepository
from app.db.repository.user_repo import UserRepository
from app.db.models.sos import Sos
from app.db.schemas.sos import User_clicks_sos
from fastapi import HTTPException
from geoalchemy2.elements import WKTElement


class SosService:
        def __init__(self,session: Session):
            self.__userRepo = UserRepository(session=session)
            self.__sosRepo = SosRepo(session = session)
            self.__guardianRepo = GuardianRepository(session=session)
            
        def refresh_sosid(self,user_id:int):
            if self.__userRepo.check_user_by_id(user_id=user_id):
                while True:
                    new_api = API_generator.generate_secure_string(16)
                    user = self.__sosRepo.check_user_by_sos_id(new_api)
                    if not user:
                        self.__sosRepo.update_sos_id(user_id,new_api)
                        return {"new_sos_id":new_api}
                
        def create_sos_event(self,user_id:int,sos_info:User_clicks_sos):
             user = self.__userRepo.check_user_by_id(user_id=user_id)
             if user:
                point = WKTElement(
                     f"POINT({sos_info.longitude} {sos_info.latitude})",
                     srid=4326
                )
                create_sos = Sos(
                    user_id = user.id,
                    location = point,
                    status = "active"
                )
                self.__sosRepo.create_sos_event(create_sos)
                return {"message":"SOS created"}
             raise HTTPException(status_code=400,detail="User not found")
        
        # def sos_info_sender(self,user_id:int):
        #      if not self.__userRepo.check_user_by_id(user_id=user_id):
        #           raise HTTPException(status_code=400,detail="User not found")
        #      user_data_from_sos_table = self.__sosRepo.check_user_by_id(user_id=user_id)
        #      user_data_from_user_table = self.__userRepo.check_user_by_id(user_id=user_id)
        #      user_data_from_guardian_table_list = self.__guardianRepo.get_guardian(user_id=user_id)
             

