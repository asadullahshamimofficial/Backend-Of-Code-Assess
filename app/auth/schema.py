from pydantic import BaseModel, Field


class SignupRequest(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    email: str
    password: str = Field(min_length=6, max_length=100)


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshRequest(BaseModel):
    refresh_token: str = Field(min_length=1)


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str = Field(min_length=1)
    new_password: str = Field(min_length=6, max_length=100)


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    profile_image: str | None
    is_active: bool
    model_config = {"from_attributes": True}
