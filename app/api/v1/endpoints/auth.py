from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from core.security import (get_password_hash, 
                           verify_password, 
                           create_access_token, 
                           create_refresh_token, 
                           decode_token,
                           create_reset_password_token,
                           verify_reset_password_token)

from db.repositories.user import UserRepository
from db.dependency import get_database
from db.models.user import User, UserCreate
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

class LoginRequest(BaseModel):
    username: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    first_name: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

@router.post("/register")
async def register_user(user_create: UserCreate, db=Depends(get_database)):
    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_email(user_create.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user_create.password)
    user_data = user_create.dict()
    user_data.pop("password")  # Remove plain-text password
    user_in_db = User(**user_data, 
                      hashed_password=hashed_password,
                      created_at=datetime.utcnow(), 
                      updated_at=datetime.utcnow())
    
    await user_repo.create_user(user_in_db)
    return {"msg": "User registered successfully"}

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_database)):
    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user["email"]})
    refresh_token = create_refresh_token(data={"sub": user["email"]})
    
    return {
            "access_token": access_token, 
            "refresh_token": refresh_token, 
            "token_type": "bearer",
            "first_name": user.get("first_name"),
            }

async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_database)):
    token_data = decode_token(token)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_email(token_data.email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# @router.post("/forgot-password")
# async def forgot_password(request: PasswordResetRequest, db=Depends(get_database)):
#     user_repo = UserRepository(db)
#     user = await user_repo.get_user_by_email(request.email)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     token = create_reset_password_token(user.email)
#     await send_reset_password_email(user.email, token)
#     return {"msg": "Password reset email sent"}

# @router.post("/reset-password")
# async def reset_password(request: PasswordResetConfirm, db=Depends(get_database)):
#     email = verify_reset_password_token(request.token)
#     if not email:
#         raise HTTPException(status_code=400, detail="Invalid or expired token")
#     user_repo = UserRepository(db)
#     user = await user_repo.get_user_by_email(email)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     hashed_password = get_password_hash(request.new_password)
#     await user_repo.update_password(email, hashed_password)
#     return {"msg": "Password has been reset"}
