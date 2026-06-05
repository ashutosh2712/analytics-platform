from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.repositories.dashboard_repository import (
    DashboardRepository,
)

from app.repositories.widget_repository import (
    WidgetRepository,
)

from app.schemas.widget import (
    CreateWidgetRequest,
)


class WidgetService:

    @staticmethod
    async def create_widget(
        db: AsyncSession,
        organization_id: int,
        payload: CreateWidgetRequest,
    ):

        dashboard = (
            await DashboardRepository.get_by_id(
                db=db,
                dashboard_id=payload.dashboard_id,
            )
        )

        if not dashboard:
            raise ValueError(
                "Dashboard not found"
            )

        if (
            dashboard.organization_id
            != organization_id
        ):
            raise ValueError(
                "Unauthorized access"
            )

        widget = await WidgetRepository.create(
            db=db,
            dashboard_id=payload.dashboard_id,
            title=payload.title,
            chart_type=payload.chart_type,
            metric=payload.metric,
        )

        await db.commit()

        return widget

    @staticmethod
    async def get_widgets(
        db: AsyncSession,
        organization_id: int,
        dashboard_id: int,
    ):

        dashboard = (
            await DashboardRepository.get_by_id(
                db=db,
                dashboard_id=dashboard_id,
            )
        )

        if not dashboard:
            raise ValueError(
                "Dashboard not found"
            )

        if (
            dashboard.organization_id
            != organization_id
        ):
            raise ValueError(
                "Unauthorized access"
            )

        return await WidgetRepository.get_by_dashboard(
            db=db,
            dashboard_id=dashboard_id,
        )

    @staticmethod
    async def delete_widget(
        db: AsyncSession,
        organization_id: int,
        widget_id: int,
    ):

        widget = (
            await WidgetRepository.get_by_id(
                db=db,
                widget_id=widget_id,
            )
        )

        if not widget:
            raise ValueError(
                "Widget not found"
            )

        dashboard = (
            await DashboardRepository.get_by_id(
                db=db,
                dashboard_id=widget.dashboard_id,
            )
        )

        if (
            dashboard.organization_id
            != organization_id
        ):
            raise ValueError(
                "Unauthorized access"
            )

        await WidgetRepository.delete(
            db=db,
            widget=widget,
        )

        await db.commit()

        return {
            "message": "Widget deleted"
        }