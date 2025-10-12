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


tintuc_router = APIRouter()
repo = CrudRepository(config.COLLECTION_TINTUC)
controller = BaseItemController(repo)


@tintuc_router.post("/create", response_model=CreateItemResponse)
async def create_tin_tuc(
  payload: CreateItemReqBody,
  _access_token_admin: Annotated[TokenPayload, Depends(AuthAdminRequest.access_token_admin)],
  _verified_admin: Annotated[None, Depends(AuthAdminRequest.verified_admin)],
):
  return await controller.create(payload)


@tintuc_router.put("/update", response_model=UpdateItemResponse)
async def update_tin_tuc(
  payload: UpdateItemReqBody,
  _access_token_admin: Annotated[TokenPayload, Depends(AuthAdminRequest.access_token_admin)],
  _verified_admin: Annotated[None, Depends(AuthAdminRequest.verified_admin)],
):
  return await controller.update(payload)


@tintuc_router.get("/list_rows", response_model=ListItemResponse)
async def list_tin_tuc(
  payload: ListItemReqQuery = Depends(),
  # _access_token_admin: TokenPayload = Depends(AuthAdminRequest.access_token_admin),
  # _verified_admin: None = Depends(AuthAdminRequest.verified_admin),
):
  return await controller.list(payload)


@tintuc_router.get("/detail/{id}", response_model=DetailItemResponse)
async def detail_tin_tuc(
  id: str,
  # _access_token_admin: Annotated[TokenPayload, Depends(AuthAdminRequest.access_token_admin)],
  # _verified_admin: Annotated[None, Depends(AuthAdminRequest.verified_admin)],
):
  return await controller.detail(id)


@tintuc_router.delete("/delete-one", response_model=DeleteOneItemResponse)
async def delete_one_tin_tuc(
  payload: DeleteOneItemReqBody,
  _access_token_admin: Annotated[TokenPayload, Depends(AuthAdminRequest.access_token_admin)],
  _verified_admin: Annotated[None, Depends(AuthAdminRequest.verified_admin)],
):
  return await controller.delete_one(payload)


@tintuc_router.delete("/delete-many", response_model=DeleteManyItemResponse)
async def delete_many_tin_tuc(
  payload: DeleteManyItemReqBody,
  _access_token_admin: Annotated[TokenPayload, Depends(AuthAdminRequest.access_token_admin)],
  _verified_admin: Annotated[None, Depends(AuthAdminRequest.verified_admin)],
):
  return await controller.delete_many(payload)


@tintuc_router.post(URL_UPLOAD_IMAGES_ADMIN, response_model=UploadImagesResponse)
async def upload_images_tin_tuc(
  files: List[UploadFile] = File(...),
):
  return await controller.upload_images(files)
