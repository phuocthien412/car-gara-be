from typing import Annotated
from fastapi import APIRouter, Depends
from src.dto.deps_request import AuthAdminRequest, TokenPayload
from src.controllers.items import BaseItemController
from src.repository.crud import CrudRepository
from src.dto.item_request import CreateItemReqBody, UpdateItemReqBody, ListItemReqQuery, DeleteOneItemReqBody, DeleteManyItemReqBody
from src.dto.item_response import CreateItemResponse, UpdateItemResponse, ListItemResponse, DetailItemResponse, DeleteOneItemResponse, DeleteManyItemResponse
from src.constants.config import config


duan_router = APIRouter()
repo = CrudRepository(config.COLLECTION_DUAN)
controller = BaseItemController(repo)


@duan_router.post("/create", response_model=CreateItemResponse)
async def create_du_an(
  payload: CreateItemReqBody,
  _access_token_admin: Annotated[TokenPayload, Depends(AuthAdminRequest.access_token_admin)],
  _verified_admin: Annotated[None, Depends(AuthAdminRequest.verified_admin)],
):
  return await controller.create(payload)


@duan_router.put("/update", response_model=UpdateItemResponse)
async def update_du_an(
  payload: UpdateItemReqBody,
  _access_token_admin: Annotated[TokenPayload, Depends(AuthAdminRequest.access_token_admin)],
  _verified_admin: Annotated[None, Depends(AuthAdminRequest.verified_admin)],
):
  return await controller.update(payload)


@duan_router.get("/list_rows", response_model=ListItemResponse)
async def list_du_an(
  payload: ListItemReqQuery = Depends(),
  # _access_token_admin: TokenPayload = Depends(AuthAdminRequest.access_token_admin),
  # _verified_admin: None = Depends(AuthAdminRequest.verified_admin),
):
  return await controller.list(payload)


@duan_router.get("/detail/{id}", response_model=DetailItemResponse)
async def detail_du_an(
  id: str,
  # _access_token_admin: Annotated[TokenPayload, Depends(AuthAdminRequest.access_token_admin)],
  # _verified_admin: Annotated[None, Depends(AuthAdminRequest.verified_admin)],
):
  return await controller.detail(id)


@duan_router.delete("/delete-one", response_model=DeleteOneItemResponse)
async def delete_one_du_an(
  payload: DeleteOneItemReqBody,
  _access_token_admin: Annotated[TokenPayload, Depends(AuthAdminRequest.access_token_admin)],
  _verified_admin: Annotated[None, Depends(AuthAdminRequest.verified_admin)],
):
  return await controller.delete_one(payload)


@duan_router.delete("/delete-many", response_model=DeleteManyItemResponse)
async def delete_many_du_an(
  payload: DeleteManyItemReqBody,
  _access_token_admin: Annotated[TokenPayload, Depends(AuthAdminRequest.access_token_admin)],
  _verified_admin: Annotated[None, Depends(AuthAdminRequest.verified_admin)],
):
  return await controller.delete_many(payload)

