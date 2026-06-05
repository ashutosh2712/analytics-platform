from datetime import datetime

from app.core.sync_database import (
    SessionLocal,
)

from app.models.event import Event

import app.models

from app.workers.celery_app import (
    celery_app,
)


@celery_app.task
def process_event(
    organization_id: int,
    event_name: str,
    timestamp: str,
    properties: dict,
):

    print("TASK RECEIVED")

    db = SessionLocal()

    try:

        event = Event(
            organization_id=organization_id,
            event_name=event_name,
            timestamp=datetime.fromisoformat(
                timestamp.replace("Z", "+00:00")
            ),
            properties=properties,
        )

        db.add(event)

        db.commit()

        print("EVENT SAVED")

    except Exception as e:

        db.rollback()

        print("TASK ERROR:", str(e))

        raise

    finally:

        db.close()