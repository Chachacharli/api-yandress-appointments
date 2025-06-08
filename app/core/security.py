from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/google")


def create_access_token(data: dict, expires_delta=None):
    from datetime import datetime, timedelta

    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=1))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return {
            "user_id": payload.get("sub"),
            "role": payload.get("role", "user"),
        }
    except JWTError as err:
        raise HTTPException(status_code=401, detail="Token inválido") from err


def require_admin(user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Permisos insuficientes")
    return user
