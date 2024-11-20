from fastapi import APIRouter, Depends, HTTPException, Body
from app.middleware.auth_middleware import verify_token, auth_required
from app.models.user_model import UserResponse, ErrorResponse, CreateUserRequest, LoginRequest
from firebase_admin import auth
from typing import Dict

router = APIRouter()

@router.get("/", response_model=dict)
async def root():
    return {"message": "Welcome to API Authentication with FastAPI and Firebase"}

@router.post("/register", response_model=UserResponse)
async def create_user(user_data: CreateUserRequest):
    try:
        user = auth.create_user(
            email=user_data.email,
            password=user_data.password,
            display_name=user_data.name,
            disabled=False
        )
        return UserResponse(
            uid=user.uid,
            email=user.email,
            name=user.display_name,
            photo_url=user.photo_url
        )
    except auth.EmailAlreadyExistsError:
        raise HTTPException(
            status_code=400,
            detail="Email sudah terdaftar"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error saat membuat user: {str(e)}"
        )

@router.post("/login", response_model=Dict)
async def custom_token(login_data: LoginRequest):
    try:
        user = auth.get_user_by_email(login_data.email)
        custom_token = auth.create_custom_token(user.uid)
        return {
            "token": custom_token.decode(),
            "message": "Token berhasil dibuat"
        }
    except auth.UserNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="User tidak ditemukan"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error saat login: {str(e)}"
        )

@router.get(
    "/me", 
    response_model=UserResponse,
    responses={
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse}
    }
)
@auth_required
async def get_current_user(token = Depends(verify_token)):
    try:
        user = auth.get_user(token['uid'])
        return UserResponse(
            uid=user.uid,
            email=user.email,
            name=user.display_name,
            photo_url=user.photo_url
        )
    except auth.UserNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Pengguna tidak ditemukan"
        )