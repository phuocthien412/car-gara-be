from typing import Annotated
from fastapi import APIRouter, Depends
from src.dto.deps_request import AuthAdminRequest, TokenPayload
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
from src.constants.config import config
from src.models.lien_he import LienHeModel
from src.controllers.lien_he import LienHeController


lienhe_router = APIRouter()
repo = CrudRepository(config.COLLECTION_LIENHE, LienHeModel)
controller = LienHeController(repo)


@lienhe_router.post("/create", response_model=CreateLienHeResponse)
async def create_lien_he(
  payload: CreateLienHeReqBody,
  _access_token_admin: Annotated[TokenPayload, Depends(AuthAdminRequest.access_token_admin)],
  _verified_admin: Annotated[None, Depends(AuthAdminRequest.verified_admin)],
):
  return await controller.create(payload)


@lienhe_router.put("/update", response_model=UpdateLienHeResponse)
async def update_lien_he(
  payload: UpdateLienHeReqBody,
  _access_token_admin: Annotated[TokenPayload, Depends(AuthAdminRequest.access_token_admin)],
  _verified_admin: Annotated[None, Depends(AuthAdminRequest.verified_admin)],
):
  return await controller.update(payload)


@lienhe_router.get("/list_rows", response_model=ListLienHeResponse)
async def list_lien_he(
  payload: ListLienHeReqQuery = Depends(),
):
  return await controller.list(payload)


@lienhe_router.get("/detail/{id}", response_model=DetailLienHeResponse)
async def detail_lien_he(
  id: str,
):
  return await controller.detail(id)


@lienhe_router.delete("/delete-one", response_model=DeleteOneLienHeResponse)
async def delete_one_lien_he(
  payload: DeleteOneLienHeReqBody,
  _access_token_admin: Annotated[TokenPayload, Depends(AuthAdminRequest.access_token_admin)],
  _verified_admin: Annotated[None, Depends(AuthAdminRequest.verified_admin)],
):
  return await controller.delete_one(payload)


@lienhe_router.delete("/delete-many", response_model=DeleteManyLienHeResponse)
async def delete_many_lien_he(
  payload: DeleteManyLienHeReqBody,
  _access_token_admin: Annotated[TokenPayload, Depends(AuthAdminRequest.access_token_admin)],
  _verified_admin: Annotated[None, Depends(AuthAdminRequest.verified_admin)],
):
  return await controller.delete_many(payload)

