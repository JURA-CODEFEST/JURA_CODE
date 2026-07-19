from fastapi import APIRouter,Depends
from app.db.schemas.fcm_token import Recieve_FCM
from app.utils.protectroute import get_current_user
from app.db.schemas.users import UserOutput
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.service.fcmService import FcmService


fcm = APIRouter()
@fcm.post("/user/fcm-token")
def save_fcm_token(fcm_token:Recieve_FCM,current_user:UserOutput=Depends(get_current_user),session:Session=Depends(get_db)):
    return FcmService(session=session).save_fcm(user_id=current_user.id,fcm_token=fcm_token.fcm_token)