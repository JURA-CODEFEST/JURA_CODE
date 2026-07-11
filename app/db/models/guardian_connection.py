from app.core.database import Base
from sqlalchemy import Column,Integer,String,ForeignKey

class GuardianConnection(Base):
    __tablename__ = "Guardian"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("Users.id"),nullable=False)
    guardian_id = Column(Integer,ForeignKey("Users.id"),nullable=False)
