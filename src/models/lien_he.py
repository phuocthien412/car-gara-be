from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from bson import ObjectId
from src.models.commons import PyObjectId


class LienHeModel(BaseModel):
  id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
  name: Optional[str] = None
  email: Optional[str] = None
  hotline: Optional[str] = None
  phone: Optional[str] = None
  address: Optional[str] = None
  working_hours: Optional[str] = None
  created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
  updated_at: Optional[datetime] = None

  model_config = ConfigDict(
    populate_by_name=True,
    arbitrary_types_allowed=True,
    json_encoders={ObjectId: str}
  )
