from app.core.database import Base
from sqlalchemy import Column,Integer,String,ForeignKey
from app.db.models.users import User

class UserDeviceFCM(Base):
    __tablename__ = "FCMtable"
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey(User.id),nullable=False)
    fcm_token = Column(String,nullable=False)