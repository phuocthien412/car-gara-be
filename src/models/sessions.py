from datetime import datetime, timezone
from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict
from src.models.commons import PyObjectId

class SessionsModel(BaseModel):
  id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
  end_type: str = None
  status: str = None
  started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
  model_config = ConfigDict(
    populate_by_name=True,
    arbitrary_types_allowed=True,
    json_encoders={ObjectId: str}
  )