from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
)

from app.core.dependencies import (
    require_role,
)

from app.models.enums import Role

from app.schemas.csv_upload import (
    CSVUploadResponse,
)

from app.services.csv_service import (
    CSVService,
)


router = APIRouter(
    prefix="/uploads",
    tags=["Uploads"],
)


@router.post(
    "/csv",
    response_model=CSVUploadResponse,
)
async def upload_csv(
    file: UploadFile = File(...),

    membership = Depends(
        require_role(Role.ANALYST)
    ),
):

    return await CSVService.process_csv(
        file=file,
        organization_id=
            membership.organization_id,
    )