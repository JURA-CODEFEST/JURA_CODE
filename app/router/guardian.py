from fastapi import APIRouter,Depends
from app.core.database import get_db
from app.utils.protectroute import get_current_user
from sqlalchemy.orm import Session
from app.db.schemas.guardians import Addguardian
from app.service.guardianService import GuardianService

guardian = APIRouter()

@guardian.post("/guardian/add")
def add_guardian(guardian_data:Addguardian,session : Session=Depends(get_db),current_user = Depends(get_current_user)):
    try:
        return GuardianService(session=session).connect_guardian(sos_id=guardian_data.sos_id,user_id=current_user.id)
    
    except Exception as error:
        print(error)
        raise error  