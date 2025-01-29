from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.jwt import verify_access_token
from app.services.user_service import UserService
from sqlalchemy.orm import Session
from app.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    payload = verify_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = UserService.get_user_by_id(db, int(payload["sub"]))

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
