from pydantic import BaseModel, ConfigDict


class Schema(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        from_attributes=True,
    )


class ErrorSchema(Schema):
    error: str


class PaginationSchema(Schema):
    page_number: int
    page_size: int
    total_pages: int
    total_records: int
