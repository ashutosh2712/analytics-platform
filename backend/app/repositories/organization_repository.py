from sqlalchemy.ext.asyncio import AsyncSession

from app.models.organization import Organization


class OrganizationRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        name: str,
    ) -> Organization:

        organization = Organization(
            name=name,
        )

        db.add(organization)

        await db.flush()

        await db.refresh(organization)

        return organization