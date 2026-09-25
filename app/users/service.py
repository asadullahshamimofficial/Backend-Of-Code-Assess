from sqlalchemy.orm import Session
from app.database.models import User

def get_users(db: Session, search: str | None = None, role: str | None = None, is_active: bool | None = None, skip: int = 0, limit: int = 100):
    query = db.query(User)
    if search:
        query = query.filter((User.name.ilike(f"%{search}%")) | (User.email.ilike(f"%{search}%")))
    if role:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    total = query.count()
    users = query.offset(skip).limit(limit).all()
    return users, total

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def update_user_role(db: Session, user: User, role: str):
    user.role = role
    db.commit()
    db.refresh(user)
    return user

def toggle_user_status(db: Session, user: User):
    user.is_active = not user.is_active
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()
