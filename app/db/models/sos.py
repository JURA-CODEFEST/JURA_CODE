from app.core.database import Base
from sqlalchemy import Column,String, Integer,ForeignKey, Float

class Sos(Base):
    __tablename__ = "SOS"
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey("Users.id"))
    latitude = Column(Float)
    longitude = Column(Float)
    status = Column(String(20))