from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.services.auth import (
    create_access_token,
    get_or_create_user,
    verify_google_token,
)

router = APIRouter(tags=["auth"])


@router.post("/auth/google")
def login_with_google(id_token: str):
    user_info = verify_google_token(id_token)

    user = get_or_create_user(user_info["email"], user_info["name"])

    token = create_access_token({"sub": user.id, "role": user.role})

    return JSONResponse({"access_token": token, "token_type": "bearer"})
