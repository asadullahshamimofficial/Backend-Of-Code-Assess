from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.database.models import User

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email.ilike(email.strip())).first()

def get_user_by_name(db: Session, name: str):
    return db.query(User).filter(User.name == name.strip()).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, name: str, email: str, password: str):
    user = User(name=name.strip(), email=email.strip().lower(), password=hash_password(password), role="user", is_active=True)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password) or not user.is_active:
        return None
    return user

def create_tokens(user: User):
    data = {"sub": str(user.id), "role": user.role}
    return {"access_token": create_access_token(data), "refresh_token": create_refresh_token(data), "token_type": "bearer"}

def refresh_access_token(db: Session, refresh_token: str):
    payload = decode_token(refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")
    user = get_user_by_id(db, int(payload.get("sub", 0)))
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    return create_access_token({"sub": str(user.id), "role": user.role})

def reset_user_password(db: Session, email: str, new_password: str):
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="No user found with this email")
    user.password = hash_password(new_password)
    db.commit()