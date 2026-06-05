from datetime import datetime

from pydantic import BaseModel


class CreateWidgetRequest(BaseModel):

    dashboard_id: int

    title: str

    chart_type: str

    metric: str


class WidgetResponse(BaseModel):

    id: int

    title: str

    chart_type: str

    metric: str

    created_at: datetime

    model_config = {
        "from_attributes": True
    }