from sqlalchemy.ext.asyncio import AsyncSession

from app.core.jwt import (
    create_access_token,
    create_refresh_token,
)

from app.core.security import (
    hash_password,
    verify_password,
)

from app.models.enums import Role

from app.repositories.user_repository import (
    UserRepository,
)

from app.repositories.organization_repository import (
    OrganizationRepository,
)

from app.repositories.membership_repository import (
    MembershipRepository,
)

from app.schemas.auth import (
    SignupRequest,
    LoginRequest,
    TokenResponse,
)


class AuthService:

    @staticmethod
    async def signup(
        db: AsyncSession,
        payload: SignupRequest,
    ) -> TokenResponse:

        # CHECK EXISTING USER
        existing_user = await UserRepository.get_by_email(
            db=db,
            email=payload.email,
        )

        if existing_user:

            raise ValueError(
                "User already exists"
            )

        # HASH PASSWORD
        password_hash = hash_password(
            payload.password
        )

        try:

            # CREATE USER
            user = await UserRepository.create(
                db=db,
                email=payload.email,
                password_hash=password_hash,
            )

            # CREATE ORGANIZATION
            organization = (
                await OrganizationRepository.create(
                    db=db,
                    name=payload.organization_name,
                )
            )

            # CREATE MEMBERSHIP
            membership = (
                await MembershipRepository.create(
                    db=db,
                    user_id=user.id,
                    organization_id=organization.id,
                    role=Role.OWNER,
                )
            )

            # COMMIT TRANSACTION
            await db.commit()

            # GENERATE TOKENS
            access_token = create_access_token(
                user.id
            )

            refresh_token = create_refresh_token(
                user.id
            )

            return TokenResponse(

                access_token=access_token,

                refresh_token=refresh_token,

                token_type="bearer",

                role=membership.role.value,
            )

        except Exception as e:

            await db.rollback()

            raise e

    @staticmethod
    async def login(
        db: AsyncSession,
        payload: LoginRequest,
    ) -> TokenResponse:

        user = await UserRepository.get_by_email(
            db=db,
            email=payload.email,
        )

        if not user:
            raise ValueError(
                "Invalid credentials"
            )

        is_valid_password = verify_password(
            payload.password,
            user.password_hash,
        )

        if not is_valid_password:
            raise ValueError(
                "Invalid credentials"
            )
            
        membership = user.memberships[0]

        access_token = create_access_token(
            user.id
        )

        refresh_token = create_refresh_token(
            user.id
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            role=membership.role,
        )