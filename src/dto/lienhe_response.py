from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class LienHeResponseDict(BaseModel):
  id: str = Field(default_factory=str, alias="_id")
  name: Optional[str] = None
  email: Optional[str] = None
  hotline: Optional[str] = None
  phone: Optional[str] = None
  address: Optional[str] = None
  working_hours: Optional[str] = None
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None


class ListLienHeResponsePagination(BaseModel):
  data: List[LienHeResponseDict]
  page: int
  limit: int
  total_pages: int


class ListLienHeResponse(BaseModel):
  msg: str
  data: ListLienHeResponsePagination


class CreateLienHeResponse(BaseModel):
  msg: str
  data: LienHeResponseDict


class UpdateLienHeResponse(CreateLienHeResponse):
  pass


class DetailLienHeResponse(BaseModel):
  msg: str
  data: LienHeResponseDict


class DeleteOneLienHeResponse(BaseModel):
  msg: str


class DeleteManyLienHeResponse(DeleteOneLienHeResponse):
  pass
