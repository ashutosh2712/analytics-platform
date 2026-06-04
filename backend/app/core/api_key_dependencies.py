from fastapi import (
    Header,
    HTTPException,
    status,
    Depends,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.core.database import get_db

from app.core.security import (
    verify_api_key,
)

from app.repositories.api_key_repository import (
    ApiKeyRepository,
)


async def get_api_key_organization(
    x_api_key: str = Header(...),
    db: AsyncSession = Depends(get_db),
):

    api_keys = await ApiKeyRepository.get_all_active(
        db=db
    )

    for api_key in api_keys:

        is_valid = verify_api_key(
            x_api_key,
            api_key.key_hash,
        )

        if is_valid:
            return api_key.organization_id

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
    )