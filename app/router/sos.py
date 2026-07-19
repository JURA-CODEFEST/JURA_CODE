from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.utils.protectroute import get_current_user
# from app.service.userService import UserService
from app.service.sosService import SosService
from app.db.schemas.sos import User_clicks_sos
# from app.service.reportService import ReportService

refresh_sos = APIRouter()
@refresh_sos.post("/refresh_sos_id")
def refresh_sos_id(session: Session=Depends(get_db),current_user = Depends(get_current_user)):
    try:
        return SosService(session=session).refresh_sosid(current_user.id)
    except Exception as error:
        print(error)
        raise error
    
@refresh_sos.post("/sos/trigger")
def trigger_sos(sos_info:User_clicks_sos,session:Session=Depends(get_db),current_user = Depends(get_current_user)):
    try:
        return SosService(session=session).create_sos_event(user_id=current_user.id,sos_info=sos_info)
    except Exception as error:
        print(error)
        raise error
    

@refresh_sos.get("/sos_alert")
def sos_alert(user_id:int,session:Session=Depends(get_db),current_user=Depends(get_current_user)):
    try:
        return SosService(session=session).send_sos_info_to_guardian(user_id=current_user.id)
    except Exception as error:
        print(error)
        raise error
