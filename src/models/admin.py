from datetime import datetime, timezone
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, Literal
from src.models.commons import PyObjectId
from src.constants.enum import ENUM_ADMIN_ACTIVE_STATUS, ENUM_ADMIN_INACTIVE_STATUS

class AdminModel(BaseModel):
  id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
  ho_va_ten: Optional[str] = None
  email: EmailStr
  sdt: Optional[str] = None
  password: Optional[str] = None
  vai_tro: Optional[str] = None
  ngay_sinh: Optional[datetime] = None
  trang_thai: Optional[Literal[ENUM_ADMIN_ACTIVE_STATUS, ENUM_ADMIN_INACTIVE_STATUS]] = Field(default=ENUM_ADMIN_INACTIVE_STATUS) # type: ignore
  ngay_tao_tai_khoan: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
  ngay_cap_nhat_tai_khoan: Optional[datetime] = None

  model_config = ConfigDict(
    populate_by_name=True,
    arbitrary_types_allowed=True,
    json_encoders={ObjectId: str}
  )