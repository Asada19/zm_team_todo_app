from pydantic import BaseModel, Field
from datetime import datetime


class TaskSchema(BaseModel):
    id: int = Field(None, description="ID задачи")
    created_at: datetime = Field(..., description="Дата создания задачи")
    updated_at: datetime = Field(..., description="Дата обновления задачи")
    datetime_to_do: datetime = Field(
        ..., description="Предполагаемая дата выполнения задачи"
    )
    task_info: str = Field(..., description="Описание задачи")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "created_at": "2024-09-30T12:30:00",
                "updated_at": "2024-10-01T09:15:00",
                "datetime_to_do": "2024-10-01T15:00:00",
                "task_info": "Завершить разработку API для To Do приложения.",
            }
        }
