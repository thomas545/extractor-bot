from typing import Optional, Any
from pydantic import BaseModel, Field


class OcrRequestModel(BaseModel):
    file_id: Optional[str] = None
    url: Optional[str] = None


class OcrResponseErrorModel(BaseModel):
    file_id: Optional[str] = None
    errors: Optional[Any] = None


class OcrObjectMapper(BaseModel):
    id: Optional[str] = Field(alias="_id")
    file_name: Optional[str] = None
    url: Optional[str] = None
    file_type: Optional[str] = None