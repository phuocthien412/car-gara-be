from typing import Annotated
from fastapi import APIRouter, Depends
from src.dto.deps_request import AuthAdminRequest, TokenPayload
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
from src.constants.config import config
from src.models.my_video import MyVideoModel
from src.controllers.my_video import MyVideoController


myvideo_router = APIRouter()
repo = CrudRepository(config.COLLECTION_VIDEO, MyVideoModel)
controller = MyVideoController(repo)


@myvideo_router.post("/create", response_model=CreateMyVideoResponse)
async def create_my_video(
  payload: CreateMyVideoReqBody,
  _access_token_admin: Annotated[TokenPayload, Depends(AuthAdminRequest.access_token_admin)],
  _verified_admin: Annotated[None, Depends(AuthAdminRequest.verified_admin)],
):
  return await controller.create(payload)


@myvideo_router.put("/update", response_model=UpdateMyVideoResponse)
async def update_my_video(
  payload: UpdateMyVideoReqBody,
  _access_token_admin: Annotated[TokenPayload, Depends(AuthAdminRequest.access_token_admin)],
  _verified_admin: Annotated[None, Depends(AuthAdminRequest.verified_admin)],
):
  return await controller.update(payload)


@myvideo_router.get("/list_rows", response_model=ListMyVideoResponse)
async def list_my_video(
  payload: ListMyVideoReqQuery = Depends(),
):
  return await controller.list(payload)


@myvideo_router.get("/detail/{id}", response_model=DetailMyVideoResponse)
async def detail_my_video(
  id: str,
):
  return await controller.detail(id)


@myvideo_router.delete("/delete-one", response_model=DeleteOneMyVideoResponse)
async def delete_one_my_video(
  payload: DeleteOneMyVideoReqBody,
  _access_token_admin: Annotated[TokenPayload, Depends(AuthAdminRequest.access_token_admin)],
  _verified_admin: Annotated[None, Depends(AuthAdminRequest.verified_admin)],
):
  return await controller.delete_one(payload)


@myvideo_router.delete("/delete-many", response_model=DeleteManyMyVideoResponse)
async def delete_many_my_video(
  payload: DeleteManyMyVideoReqBody,
  _access_token_admin: Annotated[TokenPayload, Depends(AuthAdminRequest.access_token_admin)],
  _verified_admin: Annotated[None, Depends(AuthAdminRequest.verified_admin)],
):
  return await controller.delete_many(payload)

