from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class MyVideoResponseDict(BaseModel):
  id: str = Field(default_factory=str, alias="_id")
  title: Optional[str] = None
  url: Optional[str] = None
  image: Optional[str] = None
  description: Optional[str] = None
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None


class ListMyVideoResponsePagination(BaseModel):
  data: List[MyVideoResponseDict]
  page: int
  limit: int
  total_pages: int


class ListMyVideoResponse(BaseModel):
  msg: str
  data: ListMyVideoResponsePagination


class CreateMyVideoResponse(BaseModel):
  msg: str
  data: MyVideoResponseDict


class UpdateMyVideoResponse(CreateMyVideoResponse):
  pass


class DetailMyVideoResponse(BaseModel):
  msg: str
  data: MyVideoResponseDict


class DeleteOneMyVideoResponse(BaseModel):
  msg: str


class DeleteManyMyVideoResponse(DeleteOneMyVideoResponse):
  pass

