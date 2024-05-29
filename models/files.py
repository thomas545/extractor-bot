from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_serializer

FILES_COLLECTION = "files"


class BaseFileModel(BaseModel):
    file_name: str
    url: str
    file_type: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_serializer("created_at")
    def serialize_created_at(self, created_at: datetime, _info):
        return int(created_at.timestamp())

    @field_serializer("updated_at")
    def serialize_updated_at(self, updated_at: datetime, _info):
        return int(updated_at.timestamp())


class FileResponseModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    file_name: Optional[str] = None
    url: Optional[str] = None
    file_type: Optional[str] = None


class FileResponseErrorModel(BaseModel):
    file_name: Optional[str] = None
    errors: Optional[Any] = None
