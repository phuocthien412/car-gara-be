from typing import Annotated, List
from fastapi import APIRouter, Depends, UploadFile, File
from src.dto.deps_request import AuthAdminRequest, TokenPayload
from src.controllers.items import BaseItemController
from src.repository.crud import CrudRepository
from src.dto.item_request import CreateItemReqBody, UpdateItemReqBody, ListItemReqQuery, DeleteOneItemReqBody, DeleteManyItemReqBody
from src.dto.item_response import CreateItemResponse, UpdateItemResponse, ListItemResponse, DetailItemResponse, DeleteOneItemResponse, DeleteManyItemResponse
from src.constants.config import config
from src.dto.admin_respone import UploadImagesResponse
from src.constants.path import URL_UPLOAD_IMAGES_ADMIN


dichvu_router = APIRouter()
repo = CrudRepository(config.COLLECTION_DICHVU)
controller = BaseItemController(repo)


@dichvu_router.post("/create", response_model=CreateItemResponse)
async def create_dich_vu(
  payload: CreateItemReqBody,
  _access_token_admin: Annotated[TokenPayload, Depends(AuthAdminRequest.access_token_admin)],
  _verified_admin: Annotated[None, Depends(AuthAdminRequest.verified_admin)],
):
  return await controller.create(payload)


@dichvu_router.put("/update", response_model=UpdateItemResponse)
async def update_dich_vu(
  payload: UpdateItemReqBody,
  _access_token_admin: Annotated[TokenPayload, Depends(AuthAdminRequest.access_token_admin)],
  _verified_admin: Annotated[None, Depends(AuthAdminRequest.verified_admin)],
):
  return await controller.update(payload)


@dichvu_router.get("/list_rows", response_model=ListItemResponse)
async def list_dich_vu(
  payload: ListItemReqQuery = Depends(),
  # _access_token_admin: TokenPayload = Depends(AuthAdminRequest.access_token_admin),
  # _verified_admin: None = Depends(AuthAdminRequest.verified_admin),
):
  return await controller.list(payload)


@dichvu_router.get("/detail/{id}", response_model=DetailItemResponse)
async def detail_dich_vu(
  id: str,
  # _access_token_admin: Annotated[TokenPayload, Depends(AuthAdminRequest.access_token_admin)],
  # _verified_admin: Annotated[None, Depends(AuthAdminRequest.verified_admin)],
):
  return await controller.detail(id)


@dichvu_router.delete("/delete-one", response_model=DeleteOneItemResponse)
async def delete_one_dich_vu(
  payload: DeleteOneItemReqBody,
  _access_token_admin: Annotated[TokenPayload, Depends(AuthAdminRequest.access_token_admin)],
  _verified_admin: Annotated[None, Depends(AuthAdminRequest.verified_admin)],
):
  return await controller.delete_one(payload)


@dichvu_router.delete("/delete-many", response_model=DeleteManyItemResponse)
async def delete_many_dich_vu(
  payload: DeleteManyItemReqBody,
  _access_token_admin: Annotated[TokenPayload, Depends(AuthAdminRequest.access_token_admin)],
  _verified_admin: Annotated[None, Depends(AuthAdminRequest.verified_admin)],
):
  return await controller.delete_many(payload)


@dichvu_router.post(URL_UPLOAD_IMAGES_ADMIN, response_model=UploadImagesResponse)
async def upload_images_dich_vu(
  files: List[UploadFile] = File(...),
):
  return await controller.upload_images(files)
