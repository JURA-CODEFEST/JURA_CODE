from pydantic import BaseModel

class User_clicks_sos(BaseModel):
    # user_id : int
    latitude : float
    longitude : float

class Send_info_after_sos(BaseModel):
    first_name : str
    last_name : str
    latitude : float
    longitude : float
    status : str