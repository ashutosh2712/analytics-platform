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

from app.core.dependencies import (
    get_current_user,
)

from app.schemas.auth import (
    UserResponse,
)

from fastapi.security import (
    OAuth2PasswordRequestForm,
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
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):

    try:

        payload = LoginRequest(
            email=form_data.username,
            password=form_data.password,
        )

        return await AuthService.login(
            db=db,
            payload=payload,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )
        
        
@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_me(
    current_user = Depends(get_current_user),
):

    membership = current_user.memberships[0]

    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        organization_id=membership.organization_id,
        role=membership.role.value,
    )