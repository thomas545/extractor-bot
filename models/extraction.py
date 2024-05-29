from typing import Optional, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_serializer

EXTRACTION_COLLECTION = "extractions"


class Extraction(BaseModel):
    user_id: str
    file_id: str
    query: str
    response: Any
    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at")
    def serialize_created_at(self, created_at: datetime, _info):
        return int(created_at.timestamp())

    @field_serializer("updated_at")
    def serialize_updated_at(self, updated_at: datetime, _info):
        return int(updated_at.timestamp())


class ExtractionRequestModel(Extraction):
    user_id: Optional[str] = None
    response: Optional[Any] = None
    created_at: Optional[datetime] = datetime.now(timezone.utc)
    updated_at: Optional[datetime] = datetime.now(timezone.utc)


class ExtractionResponseErrorModel(BaseModel):
    _id: Optional[str] = None
    errors: Optional[Any] = None


class ExtractionObjectMapper(BaseModel):
    id: Optional[str] = Field(alias="_id")
    user_id: Optional[str] = None
    file_id: Optional[str] = None
    query: Optional[str] = None
    response: Optional[Any] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
