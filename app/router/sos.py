from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.utils.protectroute import get_current_user
# from app.service.userService import UserService
from app.service.sosService import SosService

refresh_sos = APIRouter()
@refresh_sos.post("/refresh_sos_id")
def refresh_sos_id(session: Session=Depends(get_db),current_user = Depends(get_current_user)):
    try:
        return SosService(session=session).refresh_sosid(current_user.id)
    except Exception as error:
        print(error)
        raise error
    


