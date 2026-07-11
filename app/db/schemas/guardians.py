from pydantic import BaseModel


class Showguardian(BaseModel):
    id : int
    first_name : str
    last_name : str
    sos_id : str

    class Config:
        from_attributes = True
class Addguardian(BaseModel):
    sos_id : str
