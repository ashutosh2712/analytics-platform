from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.schemas.auth import (
    SignupRequest,
    LoginRequest,
    TokenResponse,
)

from app.services.auth_service import (
    AuthService,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/signup",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    payload: SignupRequest,
    db: AsyncSession = Depends(get_db),
):

    try:
        return await AuthService.signup(
            db=db,
            payload=payload,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db),
):

    try:
        return await AuthService.login(
            db=db,
            payload=payload,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )