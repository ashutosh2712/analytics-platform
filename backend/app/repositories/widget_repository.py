from sqlalchemy import select

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.models.widget import Widget


class WidgetRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        dashboard_id: int,
        title: str,
        chart_type: str,
        metric: str,
    ):

        widget = Widget(
            dashboard_id=dashboard_id,
            title=title,
            chart_type=chart_type,
            metric=metric,
        )

        db.add(widget)

        await db.flush()

        await db.refresh(widget)

        return widget

    @staticmethod
    async def get_by_dashboard(
        db: AsyncSession,
        dashboard_id: int,
    ):

        result = await db.execute(
            select(Widget).where(
                Widget.dashboard_id
                == dashboard_id
            )
        )

        return result.scalars().all()

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        widget_id: int,
    ):

        result = await db.execute(
            select(Widget).where(
                Widget.id == widget_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def delete(
        db: AsyncSession,
        widget: Widget,
    ):

        await db.delete(widget)