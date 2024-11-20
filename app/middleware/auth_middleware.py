from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth
from functools import wraps

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        token = credentials.credentials
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=403,
            detail=f"Token tidak valid: {str(e)}"
        )

def auth_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if 'token' not in kwargs:
            raise HTTPException(
                status_code=401, 
                detail="Token diperlukan"
            )
        return await func(*args, **kwargs)
    return wrapper
