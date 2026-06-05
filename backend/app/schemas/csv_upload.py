from pydantic import BaseModel


class CSVUploadResponse(
    BaseModel
):

    message: str

    total_rows: int