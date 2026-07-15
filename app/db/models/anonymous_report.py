from app.core.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from geoalchemy2 import Geography
from datetime import datetime

class AnonymousReport(Base):
    __tablename__ = "anonymous_reports"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String(250),nullable=False)
    description = Column(String)
    location = Column(Geography(geometry_type="POINT",srid=4326),nullable=False)
    verified = Column(Boolean, default=False,nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow,nullable=False)