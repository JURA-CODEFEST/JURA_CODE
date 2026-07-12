from app.db.repository.base_repo import BaseRepository
from app.db.models.guardian_connection import GuardianConnection
from sqlalchemy import delete

class GuardianRepository(BaseRepository):
    def create_guardian_connection(self,guardian:list[GuardianConnection]):
        self.session.add_all(guardian)
        self.session.commit()
        # self.session.refresh(guardian)
        return guardian

    def dup_connection_checker(self,guardian_id:int,user_id:int):
        user = self.session.query(GuardianConnection).filter(
            GuardianConnection.user_id == user_id,
            GuardianConnection.guardian_id == guardian_id
        ).first()
        return bool(user)
    
    def get_guardian(self,user_id:int):
        guardians = self.session.query(GuardianConnection).filter(GuardianConnection.user_id==user_id).all()
        return guardians
    
    def del_guardian(self,user_id:int,guardian_id:int):
        # guardian = self.session.query(GuardianConnection).filter(GuardianConnection.user_id==user_id).all()
        # delete_guardian = delete(GuardianConnection).where(GuardianConnection.user_id==user_id)
        # self.session.execute(delete_guardian)
        # self.session.commit()
        # for guardians in guardian:
        #     delete_guardian = delete(GuardianConnection).where(GuardianConnection.user_id==guardians.guardian_id & GuardianConnection.guardian_id==user_id)
        #     self.session.execute(delete_guardian)
        #     self.session.commit()
        # guardian = self.session.query(GuardianConnection).filter(GuardianConnection.user_id==user_id&GuardianConnection.guardian_id==guardian_id).all()
        # guardian.append(self.session.query(GuardianConnection).filter(GuardianConnection.user_id==guardian_id&GuardianConnection.guardian_id==user_id))
        # for guardians in guardian:
        #     delete_guardian = delete(GuardianConnection).where((GuardianConnection.user_id==guardians.guardian_id) & (GuardianConnection.guardian_id==user_id))
        #     self.session.execute(delete_guardian)
        #     self.session.commit()

        delete_guardian = delete(GuardianConnection).where((GuardianConnection.user_id==user_id)&(GuardianConnection.guardian_id==guardian_id))
        self.session.execute(delete_guardian)
        delete_guardian = delete(GuardianConnection).where((GuardianConnection.user_id==guardian_id)&(GuardianConnection.guardian_id==user_id))
        self.session.execute(delete_guardian)
        self.session.commit()
        return {"message":"Guardian removed successfully"}