from fastapi import Depends, Header, HTTPException, status
from app.core.security.authHandler import AuthHandler
from app.service.userService import UserService
from app.service.sosService import SosService
from app.core.database import get_db
from sqlalchemy.orm import Session
from typing import Optional
from app.db.schemas.users import UserOutput

AUTH_PREFIX = "Bearer "

def get_current_user(session: Session=Depends(get_db),authorization: Optional[str] = Header(None)):
    authException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid authentication credentials")
    if not authorization:
        raise authException
    if not authorization.startswith(AUTH_PREFIX):
        raise authException
    
    payload = AuthHandler.decodejwt(token=authorization[len(AUTH_PREFIX):])
    if payload and payload["user_id"]:
        try:
            user = UserService(session=session).get_user_by_id(payload["user_id"])
            # print(user.sos_id)
            return UserOutput(id=user.id,first_name=user.first_name,last_name=user.last_name,email=user.email,sos_id=user.sos_id,role=user.role)
        except Exception as error:
            raise error
        
def admin_check_for_privileged_endpoints(current_user: UserOutput=Depends(get_current_user)):
    # user = UserService(session=session).get_user_by_id(current_user.id)

    # if user.role == 1:
    #     return UserOutput(id=user.id,first_name=user.first_name,last_name=user.last_name,email=user.email,sos_id=user.sos_id)
            
    # raise HTTPException(
    # status_code=status.HTTP_403_FORBIDDEN,
    # detail="Admin access required"
    # )
    if current_user.role == 1:
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = "Admin access required")
