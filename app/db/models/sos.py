from app.core.database import Base
from sqlalchemy import Column,String, Integer,ForeignKey, Float
from geoalchemy2 import Geography

class Sos(Base):
    __tablename__ = "SOS"
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey("Users.id"))
    location = Column(
        Geography(geometry_type="POINT",srid=4326)
    )
    status = Column(String(20))