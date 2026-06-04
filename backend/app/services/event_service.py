from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.repositories.event_repository import (
    EventRepository,
)

from app.schemas.event import (
    EventIngestionRequest,
)

from app.workers.event_tasks import (
    process_event,
)

from dateutil.parser import isoparse

class EventService:

    @staticmethod
    async def ingest_event(
        db: AsyncSession,
        organization_id: int,
        payload: EventIngestionRequest,
    ):

        process_event.delay(
            organization_id=organization_id,
            event_name=payload.event_name,
            timestamp=payload.timestamp.isoformat(),
            properties=payload.properties,
        )

        return {
            "message": "Event queued",
        }

    @staticmethod
    async def ingest_batch_events(
        db: AsyncSession,
        organization_id: int,
        events: list[EventIngestionRequest],
    ):

        for payload in events:

            process_event.delay(
                organization_id=organization_id,
                event_name=payload.event_name,
                timestamp=payload.timestamp.isoformat(),
                properties=payload.properties,
            )

        return {
            "message": "Batch queued",
            "events_queued": len(events),
        }