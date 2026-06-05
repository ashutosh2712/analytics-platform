from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.services.analytics_service import (
    AnalyticsService,
)


class WidgetDataService:

    @staticmethod
    async def resolve_widget_data(
        db: AsyncSession,
        organization_id: int,
        metric: str,
    ):

        if metric == "count":

            return await AnalyticsService.get_total_events(
                db=db,
                organization_id=organization_id,
            )

        elif metric == "by_name":

            return await AnalyticsService.get_events_by_name(
                db=db,
                organization_id=organization_id,
            )

        elif metric == "timeseries":

            return await AnalyticsService.get_event_timeseries(
                db=db,
                organization_id=organization_id,
            )

        return {
            "message": "Unknown metric"
        }