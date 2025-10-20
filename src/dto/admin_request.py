import re
from pydantic_core import core_schema
from fastapi import Query
from datetime import datetime, timezone
from bson import ObjectId
from typing import Optional, Literal, List
from pydantic import BaseModel, Field, field_validator, ConfigDict, GetCoreSchemaHandler
from src.constants.enum import ENUM_DESC
from src.constants.pagination import LIMIT, PAGE
from src.constants.regex import EMAIL_REGEX, PHONE_REGEX, PASSWORD_REGEX
from src.constants.roles import EMAIL_MAX_LENGTH, FULLNAME_MAX_LENGTH, EMAIL_MIN_LENGTH, EMPTY_STRING, PASSWORD_MAX_LENGTH, VAI_TRO_MIN_LENGTH, VAI_TRO_MAX_LENGTH, PASSWORD_MIN_LENGTH
from src.constants.messages import ERROR_DATE_OF_BIRTH_IS_ISO8601, ERROR_EMAIL_MAX_LENGTH, ERROR_FULLNAME_MAX_LENGTH,ERROR_FULLNAME_REQUIRED, ERROR_EMAIL_REQUIRED, ERROR_EMAIL_INVALID, ERROR_EMAIL_MIN_LENGTH, ERROR_IDS_ADMIN_IS_REQUIRED, ERROR_PASSWORD_MAX_LENGTH, ERROR_PHONE_NUMBER_INVALID, ERROR_VAI_TRO_REQUIRED, ERROR_DATE_OF_BIRTH_INVALID, ERROR_VAI_TRO_MIN_LENGTH, ERROR_VAI_TRO_MAX_LENGTH, ERROR_PASSWORD_REQUIRED, ERROR_PASSWORD_INVALID, ERROR_PASSWORD_MIN_LENGTH, OBJECT_ID_INVALID, ERROR_PAGINATION

class PyObjectId(ObjectId):
  @classmethod
  def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler):
    return core_schema.no_info_after_validator_function(
      cls.validate,
      core_schema.str_schema()
    )

  @classmethod
  def validate(cls, value):
    if not ObjectId.is_valid(value):
      raise ValueError(OBJECT_ID_INVALID)
    return ObjectId(value)
  @classmethod
  def __get_pydantic_json_schema__(cls, schema, handler):
    return handler(core_schema.str_schema())

class CreateAdminReqBody(BaseModel):
  email: str
  name: Optional[str] = None
  password: str
  sdt: Optional[str] = None
  vai_tro: Optional[str] = None
  ngay_sinh: Optional[datetime] = None

  @field_validator('name')
  def validate_name(cls, value):
    if value is None:
      return value
    if value.strip() == EMPTY_STRING:
      raise ValueError(ERROR_FULLNAME_REQUIRED)
    if(len(value) > FULLNAME_MAX_LENGTH):
      raise ValueError(ERROR_FULLNAME_MAX_LENGTH)
    return value
  
  @field_validator('email')
  def validate_email(cls, value):
    if not value or value.strip() == EMPTY_STRING:
      raise ValueError(ERROR_EMAIL_REQUIRED)
    if not re.match(EMAIL_REGEX, value):
      raise ValueError(ERROR_EMAIL_INVALID)
    if len(value) < EMAIL_MIN_LENGTH:
      raise ValueError(ERROR_EMAIL_MIN_LENGTH)
    return value
  
  @field_validator("sdt")
  def validate_phone(cls, value):
    pattern = re.compile(PHONE_REGEX)
    if len(value) < EMAIL_MIN_LENGTH:
      raise ValueError(ERROR_EMAIL_MIN_LENGTH)
    if not pattern.match(value):
      raise ValueError(ERROR_PHONE_NUMBER_INVALID)
    return value
  
  @field_validator('vai_tro')
  def check_vai_tro(cls, value):
    if value is None:
      return value
    if value.strip() == EMPTY_STRING:
      raise ValueError(ERROR_VAI_TRO_REQUIRED)
    if len(value) < VAI_TRO_MIN_LENGTH:
      raise ValueError(ERROR_VAI_TRO_MIN_LENGTH)
    if len(value) > VAI_TRO_MAX_LENGTH:
      raise ValueError(ERROR_VAI_TRO_MAX_LENGTH)
    return value
  
  @field_validator('ngay_sinh')
  def check_date_of_birth(cls, value: datetime):
    if value is None:
      return value
    if value > datetime.now(timezone.utc):
      raise ValueError(ERROR_DATE_OF_BIRTH_INVALID)
    return value
  
class LoginAdminReqBody(BaseModel):
  email: str
  password: str

  @field_validator('email')
  def validate_email(cls, value):
    if not value or value.strip() == EMPTY_STRING:
      raise ValueError(ERROR_EMAIL_REQUIRED)
    if not re.match(EMAIL_REGEX, value):
      raise ValueError(ERROR_EMAIL_INVALID)
    if len(value) < EMAIL_MIN_LENGTH:
      raise ValueError(ERROR_EMAIL_MIN_LENGTH)
    if len(value) > EMAIL_MAX_LENGTH:
      raise ValueError(ERROR_EMAIL_MAX_LENGTH)
    return value
  
  @field_validator('password')
  def validate_password(cls, v):
    if not v or v.strip() == EMPTY_STRING:
      raise ValueError(ERROR_PASSWORD_REQUIRED)
    if not re.match(PASSWORD_REGEX, v):
      raise ValueError(ERROR_PASSWORD_INVALID)
    if len(v) < PASSWORD_MIN_LENGTH:
      raise ValueError(ERROR_PASSWORD_MIN_LENGTH)
    if len(v) > PASSWORD_MAX_LENGTH:
      raise ValueError(ERROR_PASSWORD_MAX_LENGTH)
    return v
  
class UpdateAdminReqBody(CreateAdminReqBody):
  id: PyObjectId = Field(..., alias="_id")
  name: Optional[str] = None
  email: Optional[str] = None
  password: Optional[str] = None
  sdt: Optional[str] = None
  vai_tro: Optional[str] = None
  ngay_sinh: Optional[datetime] = None
  ngay_cap_nhat_tai_khoan: Optional[datetime] = None
  model_config = ConfigDict(
    populate_by_name=True,
    arbitrary_types_allowed=True,
    json_encoders={PyObjectId: lambda v: str(v)}
  )
  @field_validator("ngay_sinh", mode="before")
  def validate_iso8601(cls, v):
    if v is None:
      return v
    try:
      return datetime.fromisoformat(v.replace("Z", "+00:00"))
    except Exception:
      raise ValueError(ERROR_DATE_OF_BIRTH_IS_ISO8601)

class ListAdminReqQuery(BaseModel):
  page: Optional[int] = Query(default=PAGE, ge=1)
  limit: Optional[int] = Query(default=LIMIT, ge=1)
  email: Optional[str] = None
  sort_order: Literal["asc", "desc"] = ENUM_DESC
  @field_validator("page", "limit", mode="before")
  def convert_to_int_str(cls, v):
    if v is None:
      return v
    if not str(v).isdigit():
      raise ValueError(ERROR_PAGINATION)
    return v

class LoginAdminReqRepositoryBody(BaseModel):
  ma_admin: str
  trang_thai: str

class RefreshTokenReqBody(BaseModel):
  refresh_token: str

class LogoutAdminReqBody(RefreshTokenReqBody):
  pass

class DetailAdminReqParams(BaseModel):
  id: str

class DeleteOneAdminReqBody(BaseModel):
  id: str

class DeleteManyAdminReqBody(BaseModel):
  ids: List[str]
  @field_validator("ids")
  def validate_ids(cls, v):
    if not v:
      raise ValueError(ERROR_IDS_ADMIN_IS_REQUIRED)
    for i in v:
      if not isinstance(i, str):
        raise ValueError(f"id phải là string, nhận {type(i)}")
      if not ObjectId.is_valid(i):
        raise ValueError(f"id không hợp lệ: {i}")
    return v
