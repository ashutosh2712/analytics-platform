import csv
import io
import json

from fastapi import UploadFile

from app.workers.event_tasks import (
    process_event,
)


class CSVService:

    @staticmethod
    async def process_csv(
        file: UploadFile,
        organization_id: int,
    ):

        content = (
            await file.read()
        ).decode("utf-8")

        csv_reader = csv.DictReader(
            io.StringIO(content)
        )

        total_rows = 0

        for row in csv_reader:

            properties = {}

            if row.get("properties"):

                properties = json.loads(
                    row["properties"]
                )

            process_event.delay(
                organization_id,
                row["event_name"],
                row["timestamp"],
                properties,
            )

            total_rows += 1

        return {
            "message":
                "CSV uploaded successfully",

            "total_rows":
                total_rows,
        }