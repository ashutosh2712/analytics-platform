from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.core.dependencies import (
    require_role,
)

from app.models.enums import Role

from app.schemas.api_key import (
    CreateApiKeyRequest,
)

from app.services.api_key_service import (
    ApiKeyService,
)


router = APIRouter(
    prefix="/api-keys",
    tags=["API Keys"],
)


@router.post("/")
async def create_api_key(
    payload: CreateApiKeyRequest,
    membership = Depends(
        require_role(Role.ADMIN)
    ),
    db: AsyncSession = Depends(get_db),
):

    return await ApiKeyService.create_api_key(
        db=db,
        organization_id=membership.organization_id,
        name=payload.name,
    )


@router.get("/")
async def list_api_keys(
    membership = Depends(
        require_role(Role.ADMIN)
    ),
    db: AsyncSession = Depends(get_db),
):

    return await ApiKeyService.list_api_keys(
        db=db,
        organization_id=membership.organization_id,
    )
    
@router.post("/{api_key_id}/revoke")
async def revoke_api_key(
    api_key_id: int,
    membership = Depends(
        require_role(Role.ADMIN)
    ),
    db: AsyncSession = Depends(get_db),
):

    return await ApiKeyService.revoke_api_key(
        db=db,
        organization_id=membership.organization_id,
        api_key_id=api_key_id,
    )
    
@router.post("/{api_key_id}/rotate")
async def rotate_api_key(
    api_key_id: int,
    membership = Depends(
        require_role(Role.ADMIN)
    ),
    db: AsyncSession = Depends(get_db),
):

    return await ApiKeyService.rotate_api_key(
        db=db,
        organization_id=membership.organization_id,
        api_key_id=api_key_id,
    )