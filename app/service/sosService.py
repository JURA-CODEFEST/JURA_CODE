from app.core.security.api_generator import API_generator
from sqlalchemy.orm import Session
from app.db.repository.sos_repo import SosRepo
from app.db.repository.guardian_repo import GuardianRepository
from app.db.repository.user_repo import UserRepository
from app.db.models.sos import Sos
from app.db.schemas.sos import User_clicks_sos
from fastapi import HTTPException
from geoalchemy2.elements import WKTElement
# from app.db.schemas.sos import Send_info_after_sos
from app.db.repository.Fcm_repo import FCMrepository
from app.service.notificationService import NotificationService

class SosService:
        def __init__(self,session: Session):
            self.__userRepo = UserRepository(session=session)
            self.__sosRepo = SosRepo(session = session)
            self.__guardianRepo = GuardianRepository(session=session)
            self.__fcmRepo = FCMrepository(session=session)
            
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
                

                guardians = self.__guardianRepo.get_guardian(user_id=user_id)
                guardian_id = []
                for guardian in guardians:
                     guardian_id.append(guardian.guardian_id)
                
                fcm_tokens = []
                for token in guardian_id:
                     user_from_fcm = self.__fcmRepo.get_by_id(user_id=token)
                     for user_list_fcm in user_from_fcm:
                          fcm_tokens.append(user_list_fcm.fcm_token)

                if fcm_tokens:
                     NotificationService.send_sos_notification(fcm_tokens)    


                return {"message":"SOS created","tokens":fcm_tokens}
             
                     
             raise HTTPException(status_code=400,detail="User not found")
        


     #    def send_sos_info_to_guardian(self,user_id:int):
     #         user = self.__userRepo.check_user_by_id(user_id=user_id)
     #         if not user:
     #           raise HTTPException(status_code=400,detail="User not found")
             
     #         sos = self.__sosRepo.check_alert_by_id_all(user_id=user_id)
     #         if not sos:
     #           raise HTTPException(status_code=404,detail="No active SOS")
             



             



                
        

             

