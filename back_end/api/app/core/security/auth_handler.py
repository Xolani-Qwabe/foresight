import jwt
import decouple 
import time

JWT_SECRETE = '2a40f14d6a9d034275927707fa8e2e2d4a431f254d60c84a401868c16ea4a646'
JWT_ALGORITHM = 'HS256'
class AuthHandler(object):
    
    @staticmethod
    def sign_jwt(user_id: int) -> str:
        payload = {
            "user_id": user_id,
            "expires": time.time() + 24*60*60 #24hrs
        }
        token = jwt.encode(payload, JWT_SECRETE, algorithm=JWT_ALGORITHM)
        return token
    
    @staticmethod
    def decode_jwt(token: str) -> dict | None:
        try:
            decoded_token = jwt.decode(token, JWT_SECRETE, algorithms=[JWT_ALGORITHM])
            return decoded_token if decoded_token["expires"] >= time.time() else None
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            print("Invalid Token Error")
            return None