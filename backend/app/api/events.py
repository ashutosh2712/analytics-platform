from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.core.database import get_db

from app.core.api_key_dependencies import (
    get_api_key_organization,
)

from app.schemas.event import (
    EventIngestionRequest,
    BatchEventIngestionRequest,
)

from app.services.event_service import (
    EventService,
)


router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


@router.post("/")
async def ingest_event(
    payload: EventIngestionRequest,
    organization_id: int = Depends(
        get_api_key_organization
    ),
    db: AsyncSession = Depends(get_db),
):

    return await EventService.ingest_event(
        db=db,
        organization_id=organization_id,
        payload=payload,
    )


@router.post("/batch")
async def ingest_batch_events(
    payload: BatchEventIngestionRequest,
    organization_id: int = Depends(
        get_api_key_organization
    ),
    db: AsyncSession = Depends(get_db),
):

    return await EventService.ingest_batch_events(
        db=db,
        organization_id=organization_id,
        events=payload.events,
    )