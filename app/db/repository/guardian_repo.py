from app.db.repository.base_repo import BaseRepository
from app.db.models.guardian_connection import GuardianConnection

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
