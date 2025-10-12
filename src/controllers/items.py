from typing import Optional, List
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from src.repository.crud import CrudRepository
from src.dto.item_request import CreateItemReqBody, UpdateItemReqBody, ListItemReqQuery, DeleteOneItemReqBody, DeleteManyItemReqBody
from src.dto.item_response import CreateItemResponse, UpdateItemResponse, ListItemResponse, DetailItemResponse, DeleteOneItemResponse, DeleteManyItemResponse
from src.constants.messages import CREATED_SUCCESSFULLY, UPDATED_SUCCESSFULLY, DELETE_SUCCESSFULLY, UPLOAD_SUCCESSFULLY
from src.constants.config import config
from src.constants.dir import UPLOAD_DOCUMENTS_DIR
from src.dto.admin_respone import UploadImagesResponse


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

  async def upload_images(self, files: List[UploadFile]) -> UploadImagesResponse:
    allowed_extensions = set(config.ALLOWED_IMG_EXTENSIONS.split(","))
    max_file_size = int(config.MAX_FILE_SIZE_UPLOAD_IMG)
    upload_dir = Path(UPLOAD_DOCUMENTS_DIR)
    uploaded_files = []
    for file in files:
      ext = Path(file.filename).suffix.lower()
      if ext not in allowed_extensions:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"File {file.filename} không hợp lệ")
      contents = await file.read()
      if len(contents) > max_file_size:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"File {file.filename} vượt quá {max_file_size//1024//1024}MB")
      filename = f"{uuid.uuid4()}{ext}"
      save_path = upload_dir / filename
      with save_path.open("wb") as f:
        f.write(contents)
      uploaded_files.append({
        "filename": filename,
        "http": config.SERVER_URL,
        "upload_folder": UPLOAD_DOCUMENTS_DIR
      })
    return UploadImagesResponse(msg=UPLOAD_SUCCESSFULLY, data=uploaded_files)
