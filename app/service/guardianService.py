from app.db.repository.user_repo import UserRepository
from app.db.repository.sos_repo import SosRepo
from sqlalchemy.orm import Session
from app.db.schemas.guardians import Showguardian
from fastapi import HTTPException
from app.db.models.guardian_connection import GuardianConnection
from app.db.repository.guardian_repo import GuardianRepository


class GuardianService:
        def __init__(self,session: Session):
            self.__userRepo = UserRepository(session=session)
            self.__sosRepo = SosRepo(session=session)
            self.__guardianRepo = GuardianRepository(session = session)

        def connect_guardian(self,sos_id:str,user_id: int):
              user = self.__sosRepo.check_user_by_sos_id(sos_id)
              if not user:
                    raise HTTPException(status_code=400,detail="User not Found")
              guardian_id = user.id
              check = self.__guardianRepo.dup_connection_checker(guardian_id=guardian_id,user_id=user_id)
              if check:
                    raise HTTPException(status_code=400,detail="Connection already established")



              if user.id == user_id:
                    raise HTTPException(status_code=400, detail="Cannot Add yourself")
              if user:
                    connection1 = GuardianConnection(
                          user_id = user_id,# yo chahi afno userid from router (protected endpoint wala bata ako ho )
                          guardian_id = user.id # guardian ko userid after checking for user through sos_id 
                    )
                    connection2 = GuardianConnection(
                          user_id = user.id,
                          guardian_id = user_id
                    )
                    # self.__guardianRepo.create_guardian_connection(connection1)# chat ko logic ko ho hai yo
                    # self.__guardianRepo.create_guardian_connection(connection2)
                    connections = [connection1,connection2]
                    self.__guardianRepo.create_guardian_connection(connections)
                    return {"message":"Guardian connected"}

                    # return self.__guardianRepo.create_guardian_connection(connection)

        def show_guardian(self,user_id:int):
              user = self.__userRepo.check_user_by_id(user_id)
              guardian_list = []
              if not user:
                    raise HTTPException(status_code=400,detail="User not found")
              if user:
                    guardian = self.__guardianRepo.get_guardian(user_id=user_id)
                    for guardians in guardian:
                          guardian_list.append(guardians.guardian_id)
              
              guardian_info = []
              for guardian in guardian_list:
                    temp_user = self.__userRepo.check_user_by_id(guardian)
                    guardian_info.append(
                          Showguardian(
                          id = temp_user.id,
                          first_name = temp_user.first_name,
                          last_name = temp_user.last_name,
                          sos_id = temp_user.sos_id
                    )
                    )
              return guardian_info
        
        def remove_guardian(self,user_id:int,guardian_id:int):
              return self.__guardianRepo.del_guardian(user_id=user_id,guardian_id=guardian_id)
                          