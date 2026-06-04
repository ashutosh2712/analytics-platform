from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.core.database import get_db

from app.core.dependencies import (
    get_current_membership,
)

from app.services.analytics_service import (
    AnalyticsService,
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get("/events/count")
async def get_total_events(
    membership = Depends(
        get_current_membership
    ),
    db: AsyncSession = Depends(get_db),
):

    return await AnalyticsService.get_total_events(
        db=db,
        organization_id=membership.organization_id,
    )


@router.get("/events/by-name")
async def get_events_by_name(
    membership = Depends(
        get_current_membership
    ),
    db: AsyncSession = Depends(get_db),
):

    return await AnalyticsService.get_events_by_name(
        db=db,
        organization_id=membership.organization_id,
    )


@router.get("/events/timeseries")
async def get_event_timeseries(
    membership = Depends(
        get_current_membership
    ),
    db: AsyncSession = Depends(get_db),
):

    return await AnalyticsService.get_event_timeseries(
        db=db,
        organization_id=membership.organization_id,
    )