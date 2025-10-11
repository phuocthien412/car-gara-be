from typing import Optional, List
from src.repository.crud import CrudRepository
from src.dto.item_request import CreateItemReqBody, UpdateItemReqBody, ListItemReqQuery, DeleteOneItemReqBody, DeleteManyItemReqBody
from src.dto.item_response import CreateItemResponse, UpdateItemResponse, ListItemResponse, DetailItemResponse, DeleteOneItemResponse, DeleteManyItemResponse
from src.constants.messages import CREATED_SUCCESSFULLY, UPDATED_SUCCESSFULLY, DELETE_SUCCESSFULLY


class BaseItemController:
  def __init__(self, repo: CrudRepository):
    self.repo = repo

  async def create(self, payload: CreateItemReqBody) -> CreateItemResponse:
    data = await self.repo.create(payload.model_dump())
    return CreateItemResponse(msg=CREATED_SUCCESSFULLY, data=data)

  async def update(self, payload: UpdateItemReqBody) -> UpdateItemResponse:
    data = await self.repo.update(payload.id, payload.model_dump(exclude_none=True))
    return UpdateItemResponse(msg=UPDATED_SUCCESSFULLY, data=data)

  async def list(self, payload: ListItemReqQuery) -> ListItemResponse:
    result = await self.repo.list(payload.page, payload.limit, payload.q, payload.sort_order)
    return ListItemResponse(msg="OK", data=result)

  async def detail(self, id: str) -> DetailItemResponse:
    data = await self.repo.detail(id)
    return DetailItemResponse(msg="OK", data=data)

  async def delete_one(self, payload: DeleteOneItemReqBody) -> DeleteOneItemResponse:
    await self.repo.delete_one(payload.id)
    return DeleteOneItemResponse(msg=DELETE_SUCCESSFULLY)

  async def delete_many(self, payload: DeleteManyItemReqBody) -> DeleteManyItemResponse:
    await self.repo.delete_many(payload.ids)
    return DeleteManyItemResponse(msg=DELETE_SUCCESSFULLY)

