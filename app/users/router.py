from fastapi import APIRouter, HTTPException, Query, status
from app.users.schema import UserResponse, UserRoleUpdate, UserListResponse
from app.users import service
from app.core.dependencies import db_dependency, admin_dependency

router = APIRouter()

@router.get("/", response_model=UserListResponse)
def get_all_users(
    db: db_dependency,
    current_admin: admin_dependency,
    search: str | None = Query(default=None),
    role: str | None = Query(default=None),
    is_active: bool | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=50, ge=1, le=100)
):
    users, total = service.get_users(db, search=search, role=role, is_active=is_active, skip=(page - 1) * limit, limit=limit)
    return {"items": users, "total": total}

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: db_dependency, current_admin: admin_dependency):
    user = service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}/role", response_model=UserResponse)
def update_role(user_id: int, data: UserRoleUpdate, db: db_dependency, current_admin: admin_dependency):
    user = service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return service.update_user_role(db, user, data.role)

@router.put("/{user_id}/toggle-status", response_model=UserResponse)
def toggle_status(user_id: int, db: db_dependency, current_admin: admin_dependency):
    user = service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return service.toggle_user_status(db, user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: db_dependency, current_admin: admin_dependency):
    user = service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    service.delete_user(db, user)
    return None
