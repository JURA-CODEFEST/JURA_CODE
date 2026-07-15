from pydantic import BaseModel
from typing import Optional

class CreateReport(BaseModel):
    title : str
    description : Optional[str]=None
    latitude : float
    longitude : float

class ShowReport(BaseModel):
    id : int
    title: str
    description: Optional[str]=None
    latitude : float
    longitude : float
    verified : bool