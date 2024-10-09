from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth_handler import decode_jwt
from fastapi import Depends
import jwt
from app.auth.auth_handler import jwt_config
from app.database.user import retrieve_user

import logging

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decode_jwt(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True

        return isTokenValid

async def get_current_user(token: str = Depends(JWTBearer())) -> dict:
    payload = jwt.decode(token, jwt_config("secret"), algorithms=[jwt_config("algorithm")], verify_signature=False) 
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=409, detail="Invalid    token")
    user = await retrieve_user(user_id);
    user["password"] = None
    return user