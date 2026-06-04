from fastapi import (
    Depends,
    HTTPException,
    status,
)

from fastapi.security import (
    OAuth2PasswordBearer,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.core.database import get_db

from app.core.jwt import decode_token

from app.repositories.user_repository import (
    UserRepository,
)

from app.models.enums import Role

from app.repositories.membership_repository import (
    MembershipRepository,
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
    )

    try:

        payload = decode_token(token)

        user_id = payload.get("sub")

        token_type = payload.get("type")

        if token_type != "access":
            raise credentials_exception

        if not user_id:
            raise credentials_exception

        user = await UserRepository.get_by_id(
            db=db,
            user_id=int(user_id),
        )

        if not user:
            raise credentials_exception

        return user

    except Exception:
        raise credentials_exception
    
    
async def get_current_membership(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    membership = (
        await MembershipRepository.get_user_membership(
            db=db,
            user_id=current_user.id,
        )
    )

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Membership not found",
        )

    return membership


def require_role(
    minimum_role: Role,
):
    hierarchy = {
        Role.OWNER: 4,
        Role.ADMIN: 3,
        Role.ANALYST: 2,
        Role.VIEWER: 1,
    }

    async def role_checker(
        membership = Depends(
            get_current_membership
        )
    ):

        current_role = membership.role

        if (
            hierarchy[current_role]
            < hierarchy[minimum_role]
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return membership

    return role_checker