from datetime import datetime, timezone
from bson import ObjectId
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from src.models.commons import PyObjectId

class MessagesModel(BaseModel):
  id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
  role: str = None
  content: str = None
  name: Optional[str] = None
  session_id: PyObjectId = Field(default_factory=PyObjectId)
  created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
  model_config = ConfigDict(
    populate_by_name=True,
    arbitrary_types_allowed=True,
    json_encoders={ObjectId: str}
  )