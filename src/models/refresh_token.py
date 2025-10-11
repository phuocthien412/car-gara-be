from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict
from src.models.commons import PyObjectId

class RefreshTokenModel(BaseModel):
  ma_admin: PyObjectId = Field(default_factory=PyObjectId)
  token: str
  thoi_gian_het_han: datetime
  thoi_gian_tao: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
  model_config = ConfigDict(
    populate_by_name=True,
    arbitrary_types_allowed=True,
    json_encoders={PyObjectId: lambda v: str(v)}
  )