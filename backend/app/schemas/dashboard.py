from datetime import datetime

from pydantic import BaseModel


class CreateDashboardRequest(BaseModel):
    name: str


class DashboardResponse(BaseModel):

    id: int

    name: str

    created_at: datetime

    model_config = {
        "from_attributes": True
    }