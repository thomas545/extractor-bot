from typing import Optional, Any
from pydantic import BaseModel, Field


# '_id': '6654c225e8769fc30206f225', 'file_name': '東京都建築安全条例.json', 'file_type': 'json', 
# 'url': 'https://testingzone021.b-cdn.net/users_files/6651fbad0b03b201a830642a/1b38aa42-7a34-4bc9-b5fc-01c4e5f2c139.json'}



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