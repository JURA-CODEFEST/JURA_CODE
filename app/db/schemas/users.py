from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSignUp(BaseModel):
    first_name : str
    last_name : str
    email : EmailStr
    password : str

class UserOutput(BaseModel):
    id : int
    first_name : str
    last_name : str
    email : EmailStr

class UserUpdate(BaseModel):
    id : int
    first_name : Optional[str] = None
    last_name : Optional[str] = None
    email : Optional[EmailStr] = None
    password : Optional[str] = None

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class UserToken(BaseModel):
    token: str
