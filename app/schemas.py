from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


class TaskSchema(BaseModel):
    id: int = Field(None, description="ID задачи")
    created_at: datetime = Field(None, description="Дата создания задачи")
    updated_at: Optional[datetime] = Field(None, description="Дата обновления задачи")
    datetime_to_do: datetime = Field(
        description="Предполагаемая дата выполнения задачи"
    )
    task_info: str = Field(description="Описание задачи")

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class TaskCreateOrUpdateSchema(BaseModel):
    datetime_to_do: datetime = Field(
        None, description="Предполагаемая дата выполнения задачи"
    )
    task_info: Optional[str] = Field(None, description="Описание задачи")

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}
