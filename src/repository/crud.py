import re
import asyncio
from typing import Optional, Tuple, cast, List, Type
from bson import ObjectId
from fastapi import HTTPException
from pymongo import ASCENDING, DESCENDING
from starlette.status import HTTP_404_NOT_FOUND
from src.database.db import db
from src.models.item import ItemModel
from src.constants.pagination import LIMIT, PAGE
from src.constants.enum import ENUM_ASC
from src.constants.messages import ERROR_DATA_NOT_FOUND


def _serialize(doc: dict) -> dict:
  if not doc:
    return {}
  d = {**doc}
  d["_id"] = str(d["_id"]) if "_id" in d else None
  return d


class CrudRepository:
  def __init__(self, collection_name: str, model_cls: Type[ItemModel] = ItemModel):
    self.db = db
    self.collection = self.db.get_collection(collection_name)
    self.model_cls = model_cls

  async def create(self, payload: dict) -> dict:
    schema = self.model_cls(**payload)
    data_dump = schema.model_dump(by_alias=True, exclude_none=True, exclude={"id"})
    result = await self.collection.insert_one(data_dump)
    row = await self.collection.find_one({"_id": result.inserted_id})
    if not row:
      raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=ERROR_DATA_NOT_FOUND)
    return _serialize(row)

  async def update(self, id: str, payload: dict) -> dict:
    update_data = {k: v for k, v in payload.items() if v is not None and k != "id"}
    if update_data:
      from datetime import datetime, timezone
      update_data["updated_at"] = datetime.now(timezone.utc)
    row = await self.collection.find_one_and_update(
      {"_id": ObjectId(id)},
      {"$set": update_data},
      return_document=True
    )
    if not row:
      raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=ERROR_DATA_NOT_FOUND)
    return _serialize(row)

  async def detail(self, id: str) -> dict:
    row = await self.collection.find_one({"_id": ObjectId(id)})
    if not row:
      raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=ERROR_DATA_NOT_FOUND)
    return _serialize(row)

  async def delete_one(self, id: str) -> None:
    await self.collection.delete_one({"_id": ObjectId(id)})

  async def delete_many(self, ids: List[str]) -> None:
    object_ids = [ObjectId(i) for i in ids]
    await self.collection.delete_many({"_id": {"$in": object_ids}})

  async def list(self, page: Optional[int], limit: Optional[int], q: Optional[str], sort_order: str):
    page = int(page or int(PAGE))
    limit = int(limit or int(LIMIT))
    filter_query = {}
    if q:
      filter_query["title"] = {"$regex": re.escape(q), "$options": "i"}
    skip = (page - 1) * limit
    sort_direction = DESCENDING if sort_order != ENUM_ASC else ASCENDING
    data, total = await asyncio.gather(
      self.collection.find(filter_query).sort("created_at", sort_direction).skip(skip).limit(limit).to_list(length=None),
      self.collection.count_documents(filter_query)
    )
    result = [{**doc, "_id": str(doc["_id"]) } for doc in data]
    total_pages = (total + limit - 1) // limit
    return {
      "data": result,
      "page": page,
      "limit": limit,
      "total_pages": total_pages
    }
