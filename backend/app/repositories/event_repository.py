from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.models.event import Event


class EventRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        organization_id: int,
        event_name: str,
        timestamp,
        properties: dict,
    ) -> Event:

        event = Event(
            organization_id=organization_id,
            event_name=event_name,
            timestamp=timestamp,
            properties=properties,
        )

        db.add(event)

        await db.flush()

        await db.refresh(event)

        return event