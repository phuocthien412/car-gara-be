from src.repository.crud import CrudRepository
from src.dto.myvideo_request import (
  CreateMyVideoReqBody,
  UpdateMyVideoReqBody,
  ListMyVideoReqQuery,
  DeleteOneMyVideoReqBody,
  DeleteManyMyVideoReqBody,
)
from src.dto.myvideo_response import (
  CreateMyVideoResponse,
  UpdateMyVideoResponse,
  ListMyVideoResponse,
  DetailMyVideoResponse,
  DeleteOneMyVideoResponse,
  DeleteManyMyVideoResponse,
)
from src.constants.messages import CREATED_SUCCESSFULLY, UPDATED_SUCCESSFULLY, DELETE_SUCCESSFULLY


class MyVideoController:
  def __init__(self, repo: CrudRepository):
    self.repo = repo

  async def create(self, payload: CreateMyVideoReqBody) -> CreateMyVideoResponse:
    data = await self.repo.create(payload.model_dump())
    return CreateMyVideoResponse(msg=CREATED_SUCCESSFULLY, data=data)

  async def update(self, payload: UpdateMyVideoReqBody) -> UpdateMyVideoResponse:
    data = await self.repo.update(payload.id, payload.model_dump(exclude_none=True))
    return UpdateMyVideoResponse(msg=UPDATED_SUCCESSFULLY, data=data)

  async def list(self, payload: ListMyVideoReqQuery) -> ListMyVideoResponse:
    result = await self.repo.list(payload.page, payload.limit, payload.q, payload.sort_order)
    return ListMyVideoResponse(msg="OK", data=result)

  async def detail(self, id: str) -> DetailMyVideoResponse:
    data = await self.repo.detail(id)
    return DetailMyVideoResponse(msg="OK", data=data)

  async def delete_one(self, payload: DeleteOneMyVideoReqBody) -> DeleteOneMyVideoResponse:
    await self.repo.delete_one(payload.id)
    return DeleteOneMyVideoResponse(msg=DELETE_SUCCESSFULLY)

  async def delete_many(self, payload: DeleteManyMyVideoReqBody) -> DeleteManyMyVideoResponse:
    await self.repo.delete_many(payload.ids)
    return DeleteManyMyVideoResponse(msg=DELETE_SUCCESSFULLY)

