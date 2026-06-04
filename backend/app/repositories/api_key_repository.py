from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.api_key import ApiKey
from sqlalchemy import update

class ApiKeyRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        organization_id: int,
        name: str,
        key_hash: str,
    ) -> ApiKey:

        api_key = ApiKey(
            organization_id=organization_id,
            name=name,
            key_hash=key_hash,
            is_active=True,
        )

        db.add(api_key)

        await db.flush()

        await db.refresh(api_key)

        return api_key

    @staticmethod
    async def get_by_hash(
        db: AsyncSession,
        key_hash: str,
    ) -> ApiKey | None:

        result = await db.execute(
            select(ApiKey).where(
                ApiKey.key_hash == key_hash,
                ApiKey.is_active == True,
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_all_by_organization(
        db: AsyncSession,
        organization_id: int,
    ):

        result = await db.execute(
            select(ApiKey).where(
                ApiKey.organization_id
                == organization_id
            )
        )

        return result.scalars().all()
    
    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        api_key_id: int,
    ) -> ApiKey | None:

        result = await db.execute(
            select(ApiKey).where(
                ApiKey.id == api_key_id
            )
        )

        return result.scalar_one_or_none()
    
    @staticmethod
    async def revoke(
        db: AsyncSession,
        api_key: ApiKey,
    ):

        api_key.is_active = False

        await db.flush()

        await db.refresh(api_key)

        return api_key