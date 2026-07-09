from bcrypt import hashpw, checkpw , gensalt

class HashHelper:
    @staticmethod
    def gethashed(plain_password : str):
        return hashpw(plain_password.encode('utf-8'),gensalt()).decode('utf-8')
    
    @staticmethod
    def verifyhashedpassword(plain_password : str, hashed_password : str):
        if checkpw(plain_password.encode('utf-8'),hashed_password.encode('utf-8')):
            return True
        else: 
            return False