from datetime import datetime
from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    profile_image: str | None = None
    is_active: bool
    created_at: datetime
    model_config = {"from_attributes": True}


class UserRoleUpdate(BaseModel):
    role: str


class UserListResponse(BaseModel):
    items: list[UserResponse]
    total: int
