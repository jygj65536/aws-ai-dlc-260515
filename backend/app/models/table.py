"""테이블 관련 Pydantic 스키마."""

from pydantic import BaseModel, Field


class CreateTableRequest(BaseModel):
    store_id: str
    table_number: int = Field(..., ge=1, le=999)
    password: str = Field(..., min_length=4, max_length=20)


class TableResponse(BaseModel):
    table_id: str
    store_id: str
    table_number: int
    current_session_id: str | None = None


class CompleteTableResponse(BaseModel):
    success: bool = True
    message: str = "이용 완료 처리됨"


class TableHistoryResponse(BaseModel):
    history_id: str
    session_id: str
    orders: list[dict]
    total_amount: int
    completed_at: str
