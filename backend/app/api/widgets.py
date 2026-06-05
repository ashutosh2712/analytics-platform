from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.core.database import get_db

from app.core.dependencies import (
    require_role,
)

from app.models.enums import Role

from app.schemas.widget import (
    CreateWidgetRequest,
    WidgetResponse,
)

from app.services.widget_service import (
    WidgetService,
)


router = APIRouter(
    prefix="/widgets",
    tags=["Widgets"],
)


@router.post(
    "/",
    response_model=WidgetResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_widget(
    payload: CreateWidgetRequest,
    membership = Depends(
        require_role(Role.ANALYST)
    ),
    db: AsyncSession = Depends(get_db),
):

    try:

        return await WidgetService.create_widget(
            db=db,
            organization_id=membership.organization_id,
            payload=payload,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/dashboard/{dashboard_id}",
    response_model=list[WidgetResponse],
)
async def get_widgets(
    dashboard_id: int,
    membership = Depends(
        require_role(Role.VIEWER)
    ),
    db: AsyncSession = Depends(get_db),
):

    try:

        return await WidgetService.get_widgets(
            db=db,
            organization_id=membership.organization_id,
            dashboard_id=dashboard_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.delete(
    "/{widget_id}",
)
async def delete_widget(
    widget_id: int,
    membership = Depends(
        require_role(Role.ADMIN)
    ),
    db: AsyncSession = Depends(get_db),
):

    try:

        return await WidgetService.delete_widget(
            db=db,
            organization_id=membership.organization_id,
            widget_id=widget_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )