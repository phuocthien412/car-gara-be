from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from bson import ObjectId
from src.models.commons import PyObjectId


class ItemModel(BaseModel):
  id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
  title: str
  description: Optional[str] = None
  price: Optional[float] = None
  image: Optional[str] = None
  quantity: Optional[int] = 0
  in_stock: Optional[bool] = True
  created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
  updated_at: Optional[datetime] = None

  model_config = ConfigDict(
    populate_by_name=True,
    arbitrary_types_allowed=True,
    json_encoders={ObjectId: str}
  )

