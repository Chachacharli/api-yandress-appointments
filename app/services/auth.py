from datetime import datetime, timedelta

from fastapi import HTTPException
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from jose import jwt
from sqlalchemy.orm import Session

from app.core.settings import settings
from app.models.user import User

GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


def get_or_create_user(db: Session, google_info: dict) -> User:
    user = db.query(User).filter_by(user_google_id=google_info["sub"]).first()

    if not user:
        user = User(
            user_google_id=google_info["sub"],
            email=google_info["email"],
            name=google_info.get("name"),
            picture_url=google_info.get("picture"),
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return user


def verify_google_token(token: str):
    try:
        idinfo = id_token.verify_oauth2_token(
            token, google_requests.Request(), GOOGLE_CLIENT_ID
        )

        return {
            "email": idinfo["email"],
            "name": idinfo.get("name", ""),
            "picture": idinfo.get("picture", ""),
            "sub": idinfo["sub"],  # ID de Google
        }
    except Exception as err:
        raise HTTPException(status_code=401, detail="Token de Google inválido") from err


def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + expires_delta
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
