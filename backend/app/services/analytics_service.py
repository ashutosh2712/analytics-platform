from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.repositories.analytics_repository import (
    AnalyticsRepository,
)


class AnalyticsService:

    @staticmethod
    async def get_total_events(
        db: AsyncSession,
        organization_id: int,
    ):

        total = (
            await AnalyticsRepository.get_total_event_count(
                db=db,
                organization_id=organization_id,
            )
        )

        return {
            "total_events": total
        }

    @staticmethod
    async def get_events_by_name(
        db: AsyncSession,
        organization_id: int,
    ):

        rows = (
            await AnalyticsRepository.get_event_counts_by_name(
                db=db,
                organization_id=organization_id,
            )
        )

        return [
            {
                "event_name": row[0],
                "count": row[1],
            }
            for row in rows
        ]

    @staticmethod
    async def get_event_timeseries(
        db: AsyncSession,
        organization_id: int,
    ):

        rows = (
            await AnalyticsRepository.get_event_timeseries(
                db=db,
                organization_id=organization_id,
            )
        )

        return [
            {
                "date": str(row[0]),
                "count": row[1],
            }
            for row in rows
        ]