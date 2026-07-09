import jwt
import os
from dotenv import load_dotenv
import time

load_dotenv()
ALGORITHM = os.getenv("JWT_ALGORITHM")
SECRET = os.getenv("JWT_SECRET")


class AuthHandler:
    @staticmethod
    def signjwt(user_id : int):
        payload = {
            "user_id":user_id,
            "expires":time.time()+9000
        }
        token = jwt.encode(payload,SECRET,algorithm = ALGORITHM)
        return token
    @staticmethod
    def decodejwt(token : str):
        try:
            decoded_token = jwt.decode(token,SECRET,algorithms=[ALGORITHM])#decode ko lagi algorithms rw encode ko lagi algorithm
            return decoded_token if decoded_token["expires"]>=time.time() else None
        except:
            print("Unable to provide token")
            return None