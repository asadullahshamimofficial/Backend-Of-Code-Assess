from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.schema import SignupRequest, TokenResponse, UserResponse, RefreshRequest, ForgotPasswordRequest, ResetPasswordRequest
from app.auth import service
from app.core.dependencies import db_dependency, user_dependency

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def get_me(current_user: user_dependency):
    return current_user

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(data: SignupRequest, db: db_dependency):
    if service.get_user_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if service.get_user_by_name(db, data.name):
        raise HTTPException(status_code=400, detail="Username already exists")
    return service.create_user(db, data.name, data.email, data.password)

@router.post("/login", response_model=TokenResponse)
def login(db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()):
    user = service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return service.create_tokens(user)

@router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshRequest, db: db_dependency):
    new_access_token = service.refresh_access_token(db, data.refresh_token)
    return {"access_token": new_access_token, "refresh_token": data.refresh_token, "token_type": "bearer"}

@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest, db: db_dependency):
    service.generate_password_reset_token(db, data.email)
    return {"detail": "If the email exists, a reset link has been sent."}

@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest, db: db_dependency):
    service.reset_user_password(db, data.token, data.new_password)
    return {"detail": "Password has been reset successfully."}