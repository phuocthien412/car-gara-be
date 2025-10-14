from src.repository.crud import CrudRepository
from src.dto.lienhe_request import (
  CreateLienHeReqBody,
  UpdateLienHeReqBody,
  ListLienHeReqQuery,
  DeleteOneLienHeReqBody,
  DeleteManyLienHeReqBody,
)
from src.dto.lienhe_response import (
  CreateLienHeResponse,
  UpdateLienHeResponse,
  ListLienHeResponse,
  DetailLienHeResponse,
  DeleteOneLienHeResponse,
  DeleteManyLienHeResponse,
)
from src.constants.messages import CREATED_SUCCESSFULLY, UPDATED_SUCCESSFULLY, DELETE_SUCCESSFULLY


class LienHeController:
  def __init__(self, repo: CrudRepository):
    self.repo = repo

  async def create(self, payload: CreateLienHeReqBody) -> CreateLienHeResponse:
    data = await self.repo.create(payload.model_dump())
    return CreateLienHeResponse(msg=CREATED_SUCCESSFULLY, data=data)

  async def update(self, payload: UpdateLienHeReqBody) -> UpdateLienHeResponse:
    data = await self.repo.update(payload.id, payload.model_dump(exclude_none=True))
    return UpdateLienHeResponse(msg=UPDATED_SUCCESSFULLY, data=data)

  async def list(self, payload: ListLienHeReqQuery) -> ListLienHeResponse:
    result = await self.repo.list(payload.page, payload.limit, payload.q, payload.sort_order)
    return ListLienHeResponse(msg="OK", data=result)

  async def detail(self, id: str) -> DetailLienHeResponse:
    data = await self.repo.detail(id)
    return DetailLienHeResponse(msg="OK", data=data)

  async def delete_one(self, payload: DeleteOneLienHeReqBody) -> DeleteOneLienHeResponse:
    await self.repo.delete_one(payload.id)
    return DeleteOneLienHeResponse(msg=DELETE_SUCCESSFULLY)

  async def delete_many(self, payload: DeleteManyLienHeReqBody) -> DeleteManyLienHeResponse:
    await self.repo.delete_many(payload.ids)
    return DeleteManyLienHeResponse(msg=DELETE_SUCCESSFULLY)
