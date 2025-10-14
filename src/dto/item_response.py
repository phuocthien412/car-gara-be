from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ItemResponseDict(BaseModel):
  id: str = Field(default_factory=str, alias="_id")
  title: Optional[str] = None
  description: Optional[str] = None
  price: Optional[float] = None
  image: Optional[str] = None
  quantity: Optional[int] = None
  in_stock: Optional[bool] = None
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None


class ListItemResponsePagination(BaseModel):
  data: List[ItemResponseDict]
  page: int
  limit: int
  total_pages: int


class ListItemResponse(BaseModel):
  msg: str
  data: ListItemResponsePagination


class CreateItemResponse(BaseModel):
  msg: str
  data: ItemResponseDict


class UpdateItemResponse(CreateItemResponse):
  pass


class DetailItemResponse(BaseModel):
  msg: str
  data: ItemResponseDict


class DeleteOneItemResponse(BaseModel):
  msg: str


class DeleteManyItemResponse(DeleteOneItemResponse):
  pass

