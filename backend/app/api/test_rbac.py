from fastapi import APIRouter, Depends

from app.core.dependencies import (
    require_role,
)

from app.models.enums import Role


router = APIRouter(
    prefix="/rbac",
    tags=["RBAC"],
)


@router.get("/admin-only")
async def admin_only(
    membership = Depends(
        require_role(Role.ADMIN)
    )
):

    return {
        "message": "Welcome Admin",
        "role": membership.role,
    }