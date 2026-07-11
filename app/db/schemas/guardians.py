from pydantic import BaseModel


class Showguardian(BaseModel):
    guardian_id : int
    first_name : str
    last_name : str
    sos_id : str
