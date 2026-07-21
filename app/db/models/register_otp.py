from app.core.database import Base
from sqlalchemy import Column,Integer, String,ForeignKey,DateTime
from app.db.models.users import User

class OTPRegister(Base):
    __tablename__ = "registration_otp"
    id = Column(Integer,primary_key=True,nullable=False)
    user_id = Column(Integer,ForeignKey(User.id),nullable=False,unique=True)
    email = Column(String,ForeignKey(User.email),nullable=False)
    otp = Column(Integer)
    expires_at = Column(DateTime)