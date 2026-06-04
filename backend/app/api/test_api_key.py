from fastapi import (
    APIRouter,
    Depends,
)

from app.core.api_key_dependencies import (
    get_api_key_organization,
)


router = APIRouter(
    prefix="/test-api-key",
    tags=["API Key Auth"],
)


@router.get("/")
async def test_api_key(
    organization_id: int = Depends(
        get_api_key_organization
    )
):

    return {
        "organization_id": organization_id,
        "message": "API key valid",
    }