from sqlalchemy import (
    select,
    func,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.models.event import Event


class AnalyticsRepository:

    @staticmethod
    async def get_total_event_count(
        db: AsyncSession,
        organization_id: int,
    ):

        result = await db.execute(
            select(func.count(Event.id)).where(
                Event.organization_id
                == organization_id
            )
        )

        return result.scalar()

    @staticmethod
    async def get_event_counts_by_name(
        db: AsyncSession,
        organization_id: int,
    ):

        result = await db.execute(
            select(
                Event.event_name,
                func.count(Event.id).label(
                    "count"
                ),
            )
            .where(
                Event.organization_id
                == organization_id
            )
            .group_by(Event.event_name)
        )

        return result.all()

    @staticmethod
    async def get_event_timeseries(
        db: AsyncSession,
        organization_id: int,
    ):

        result = await db.execute(
            select(
                func.date(Event.timestamp).label(
                    "date"
                ),
                func.count(Event.id).label(
                    "count"
                ),
            )
            .where(
                Event.organization_id
                == organization_id
            )
            .group_by(
                func.date(Event.timestamp)
            )
            .order_by(
                func.date(Event.timestamp)
            )
        )

        return result.all()