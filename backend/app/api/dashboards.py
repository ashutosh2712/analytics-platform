from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.core.database import get_db

from app.core.dependencies import (
    require_role,
)

from app.models.enums import Role

from app.schemas.dashboard import (
    CreateDashboardRequest,
    DashboardResponse,
)

from app.services.dashboard_service import (
    DashboardService,
)


router = APIRouter(
    prefix="/dashboards",
    tags=["Dashboards"],
)


@router.post(
    "/",
    response_model=DashboardResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_dashboard(
    payload: CreateDashboardRequest,
    membership = Depends(
        require_role(Role.ANALYST)
    ),
    db: AsyncSession = Depends(get_db),
):

    try:

        return await DashboardService.create_dashboard(
            db=db,
            organization_id=membership.organization_id,
            payload=payload,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=list[DashboardResponse],
)
async def get_dashboards(
    membership = Depends(
        require_role(Role.VIEWER)
    ),
    db: AsyncSession = Depends(get_db),
):

    return await DashboardService.get_dashboards(
        db=db,
        organization_id=membership.organization_id,
    )


@router.get(
    "/{dashboard_id}",
    response_model=DashboardResponse,
)
async def get_dashboard(
    dashboard_id: int,
    membership = Depends(
        require_role(Role.VIEWER)
    ),
    db: AsyncSession = Depends(get_db),
):

    try:

        return await DashboardService.get_dashboard(
            db=db,
            organization_id=membership.organization_id,
            dashboard_id=dashboard_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.delete(
    "/{dashboard_id}",
)
async def delete_dashboard(
    dashboard_id: int,
    membership = Depends(
        require_role(Role.ADMIN)
    ),
    db: AsyncSession = Depends(get_db),
):

    try:

        return await DashboardService.delete_dashboard(
            db=db,
            organization_id=membership.organization_id,
            dashboard_id=dashboard_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
        
        
@router.get(
    "/{dashboard_id}/data",
)
async def get_dashboard_data(
    dashboard_id: int,
    membership = Depends(
        require_role(Role.VIEWER)
    ),
    db: AsyncSession = Depends(get_db),
):

    try:

        return await DashboardService.get_dashboard_data(
            db=db,
            organization_id=membership.organization_id,
            dashboard_id=dashboard_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )