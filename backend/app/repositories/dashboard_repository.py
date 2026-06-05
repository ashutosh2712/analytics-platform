from sqlalchemy import select

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.models.dashboard import Dashboard


class DashboardRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        organization_id: int,
        name: str,
    ):

        dashboard = Dashboard(
            organization_id=organization_id,
            name=name,
        )

        db.add(dashboard)

        await db.flush()

        await db.refresh(dashboard)

        return dashboard

    @staticmethod
    async def get_all(
        db: AsyncSession,
        organization_id: int,
    ):

        result = await db.execute(
            select(Dashboard).where(
                Dashboard.organization_id
                == organization_id
            )
        )

        return result.scalars().all()

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        dashboard_id: int,
    ):

        result = await db.execute(
            select(Dashboard).where(
                Dashboard.id == dashboard_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def delete(
        db: AsyncSession,
        dashboard: Dashboard,
    ):

        await db.delete(dashboard)