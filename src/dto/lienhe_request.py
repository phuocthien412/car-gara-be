from typing import Optional, Literal, List
from pydantic import BaseModel, field_validator
from bson import ObjectId
from fastapi import Query
from src.constants.pagination import LIMIT, PAGE
from src.constants.enum import ENUM_DESC
from src.constants.messages import ERROR_ID_INVALID, ERROR_PAGINATION


class CreateLienHeReqBody(BaseModel):
  name: Optional[str] = None
  hotline: Optional[str] = None
  email: Optional[str] = None
  phone: Optional[str] = None
  address: Optional[str] = None
  working_hours: Optional[str] = None


class UpdateLienHeReqBody(BaseModel):
  id: str
  name: Optional[str] = None
  hotline: Optional[str] = None
  email: Optional[str] = None
  phone: Optional[str] = None
  address: Optional[str] = None
  working_hours: Optional[str] = None

  @field_validator("id")
  @classmethod
  def validate_id(cls, v: str):
    if not ObjectId.is_valid(v):
      raise ValueError(ERROR_ID_INVALID)
    return v


class ListLienHeReqQuery(BaseModel):
  page: Optional[int] = Query(default=PAGE, ge=1)
  limit: Optional[int] = Query(default=LIMIT, ge=1)
  q: Optional[str] = None
  sort_order: Literal["asc", "desc"] = ENUM_DESC

  @field_validator("page", "limit", mode="before")
  @classmethod
  def convert_to_int_str(cls, v):
    if v is None:
      return v
    if not str(v).isdigit():
      raise ValueError(ERROR_PAGINATION)
    return v


class DeleteOneLienHeReqBody(BaseModel):
  id: str

  @field_validator("id")
  @classmethod
  def validate_id(cls, v: str):
    if not ObjectId.is_valid(v):
      raise ValueError(ERROR_ID_INVALID)
    return v


class DeleteManyLienHeReqBody(BaseModel):
  ids: List[str]

  @field_validator("ids")
  @classmethod
  def validate_ids(cls, v: List[str]):
    if not v:
      raise ValueError("ids is required")
    for i in v:
      if not isinstance(i, str) or not ObjectId.is_valid(i):
        raise ValueError(f"id invalid: {i}")
    return v
