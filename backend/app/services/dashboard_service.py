from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.repositories.dashboard_repository import (
    DashboardRepository,
)

from app.schemas.dashboard import (
    CreateDashboardRequest,
)


class DashboardService:

    @staticmethod
    async def create_dashboard(
        db: AsyncSession,
        organization_id: int,
        payload: CreateDashboardRequest,
    ):

        dashboard = (
            await DashboardRepository.create(
                db=db,
                organization_id=organization_id,
                name=payload.name,
            )
        )

        await db.commit()

        return dashboard

    @staticmethod
    async def get_dashboards(
        db: AsyncSession,
        organization_id: int,
    ):

        return await DashboardRepository.get_all(
            db=db,
            organization_id=organization_id,
        )

    @staticmethod
    async def get_dashboard(
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

        return dashboard

    @staticmethod
    async def delete_dashboard(
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

        await DashboardRepository.delete(
            db=db,
            dashboard=dashboard,
        )

        await db.commit()

        return {
            "message": "Dashboard deleted"
        }