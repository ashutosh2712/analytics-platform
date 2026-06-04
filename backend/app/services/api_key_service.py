import secrets

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password

from app.repositories.api_key_repository import (
    ApiKeyRepository,
)

from app.schemas.api_key import (
    ApiKeyResponse,
)


class ApiKeyService:

    @staticmethod
    async def create_api_key(
        db: AsyncSession,
        organization_id: int,
        name: str,
    ) -> ApiKeyResponse:

        raw_key = secrets.token_urlsafe(32)

        key_hash = hash_password(raw_key)

        api_key = await ApiKeyRepository.create(
            db=db,
            organization_id=organization_id,
            name=name,
            key_hash=key_hash,
        )

        await db.commit()

        return ApiKeyResponse(
            id=api_key.id,
            name=api_key.name,
            key=raw_key,
            is_active=api_key.is_active,
            created_at=api_key.created_at,
        )

    @staticmethod
    async def list_api_keys(
        db: AsyncSession,
        organization_id: int,
    ):

        return await ApiKeyRepository.get_all_by_organization(
            db=db,
            organization_id=organization_id,
        )
        
    @staticmethod
    async def revoke_api_key(
        db: AsyncSession,
        organization_id: int,
        api_key_id: int,
    ):

        api_key = await ApiKeyRepository.get_by_id(
            db=db,
            api_key_id=api_key_id,
        )

        if not api_key:
            raise ValueError("API key not found")

        if api_key.organization_id != organization_id:
            raise ValueError("Unauthorized")

        api_key = await ApiKeyRepository.revoke(
            db=db,
            api_key=api_key,
        )

        await db.commit()

        return {
            "message": "API key revoked"
        }
        
    @staticmethod
    async def rotate_api_key(
        db: AsyncSession,
        organization_id: int,
        api_key_id: int,
    ):

        api_key = await ApiKeyRepository.get_by_id(
            db=db,
            api_key_id=api_key_id,
        )

        if not api_key:
            raise ValueError("API key not found")

        if api_key.organization_id != organization_id:
            raise ValueError("Unauthorized")
        
        if not api_key.is_active:
            raise ValueError(
                "Cannot rotate revoked API key"
            )

        # REVOKE OLD KEY
        await ApiKeyRepository.revoke(
            db=db,
            api_key=api_key,
        )

        # GENERATE NEW KEY
        raw_key = secrets.token_urlsafe(32)

        key_hash = hash_password(raw_key)

        new_api_key = await ApiKeyRepository.create(
            db=db,
            organization_id=organization_id,
            name=f"{api_key.name} (Rotated)",
            key_hash=key_hash,
        )

        await db.commit()

        return ApiKeyResponse(
            id=new_api_key.id,
            name=new_api_key.name,
            key=raw_key,
            is_active=new_api_key.is_active,
            created_at=new_api_key.created_at,
        )