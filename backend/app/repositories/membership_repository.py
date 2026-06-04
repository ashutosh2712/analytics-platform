from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import Role
from app.models.membership import Membership

from sqlalchemy import select

from app.models.membership import Membership

class MembershipRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        user_id: int,
        organization_id: int,
        role: Role,
    ) -> Membership:

        membership = Membership(
            user_id=user_id,
            organization_id=organization_id,
            role=role,
        )

        db.add(membership)

        await db.flush()

        await db.refresh(membership)

        return membership
    
    @staticmethod
    async def get_user_membership(
        db: AsyncSession,
        user_id: int,
    ) -> Membership | None:

        result = await db.execute(
            select(Membership).where(
                Membership.user_id == user_id
            )
        )

        return result.scalar_one_or_none()