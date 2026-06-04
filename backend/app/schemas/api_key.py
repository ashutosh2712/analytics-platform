from datetime import datetime

from pydantic import BaseModel


class CreateApiKeyRequest(BaseModel):
    name: str


class ApiKeyResponse(BaseModel):
    id: int

    name: str

    key: str | None = None

    is_active: bool

    created_at: datetime

    model_config = {
        "from_attributes": True
    }