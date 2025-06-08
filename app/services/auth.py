from sqlalchemy.orm import Session

from app.models.user import User


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
