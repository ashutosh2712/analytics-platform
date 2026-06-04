from datetime import datetime
from typing import Any

from pydantic import (
    BaseModel,
    Field,
)


class EventIngestionRequest(BaseModel):

    event_name: str = Field(
        min_length=1,
        max_length=255,
    )

    timestamp: datetime

    properties: dict[str, Any] = Field(
        default_factory=dict
    )


class BatchEventIngestionRequest(
    BaseModel
):
    events: list[
        EventIngestionRequest
    ]


class EventResponse(BaseModel):

    id: int

    event_name: str

    timestamp: datetime

    properties: dict[str, Any]

    model_config = {
        "from_attributes": True
    }