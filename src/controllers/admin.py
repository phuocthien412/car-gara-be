from bson import ObjectId
import uuid
from src.constants.dir import UPLOAD_IMAGES_DIR
from src.database.db import db
from datetime import datetime, timezone
from passlib.hash import bcrypt
from src.constants.config import config
from fastapi import HTTPException, UploadFile, Request
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from src.dto.deps_request import RefreshTokenReqPayload, TokenPayload
from src.repository.admin import AdminRepository
from src.dto.admin_respone import CreateAdminResponse, DeleteManyAdminRespone, DeleteOneAdminRespone, DetailAdminRespone, ListAdminResponse, LoginAdminResponse, LogoutAdminResponse, RefreshTokenResponse, UpdateAdminResponse, UploadImagesResponse
from src.dto.admin_request import CreateAdminReqBody, DeleteManyAdminReqBody, DeleteOneAdminReqBody, DetailAdminReqParams, LoginAdminReqBody, ListAdminReqQuery, LogoutAdminReqBody, RefreshTokenReqBody, UpdateAdminReqBody
from src.constants.messages import DELETE_SUCCESSFULLY, EMAIL_IS_ALREADY, CREATED_SUCCESSFULLY, ERROR_EMAIL_NOT_FOUND, ERROR_EMAIL_OR_PASSWORD_INCORRECT, ERROR_ID_INVALID, ERROR_TOKEN_INVALID, ERROR_TOKEN_IS_REQUIRED, ERROR_TOKEN_NOT_FOUND, GET_ADMIN_SUCCESSFULLY, LOGIN_SUCCESSFULLY, ERROR_DATA_NOT_FOUND, LOGOUT_SUCCESSFULLY, REFRESH_TOKEN_SUCCESSFULLY, UPDATED_SUCCESSFULLY, UPLOAD_SUCCESSFULLY
from src.utils.jwt import verify_token
from src.utils.common import serialize_admin
from typing import List
from pathlib import Path

class AdminController:
  def __init__(self, admin_repo: AdminRepository):
    self.admin_repo = admin_repo
    self.db = db
    self.allowed_extensions = set(config.ALLOWED_IMG_EXTENSIONS.split(","))
    self.max_file_size_upload_img = int(config.MAX_FILE_SIZE_UPLOAD_IMG)
    self.upload_dir = Path(UPLOAD_IMAGES_DIR)

  async def __validate_refresh_token(self, refresh_token: str)-> bool:
    if not refresh_token: 
      raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=ERROR_TOKEN_IS_REQUIRED)
    refresh_token_result = await self.db.refresh_token.find_one({"token": refresh_token})
    if not refresh_token_result: 
      raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=ERROR_TOKEN_NOT_FOUND)
    return True

  async def login(self, payload: LoginAdminReqBody) -> LoginAdminResponse:
    row = await self.db.admin.find_one({"email": payload.email})
    if not row:
      raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail={"email": ERROR_EMAIL_NOT_FOUND})
    password_compare = bcrypt.verify(payload.password, row["password"])
    if not password_compare:
      raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail=[{"password": ERROR_EMAIL_OR_PASSWORD_INCORRECT}])
    payload = {"ma_admin": str(row['_id']), "trang_thai": row['trang_thai']}
    result = await self.admin_repo.login_repo(payload)
    return LoginAdminResponse(msg=LOGIN_SUCCESSFULLY, data=result)

  async def create_admin(self, payload: CreateAdminReqBody) -> CreateAdminResponse:
    email = await self.admin_repo.is_exist_email(payload.email)
    if email:
      raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail={"email": EMAIL_IS_ALREADY})
    data = await self.admin_repo.create_admin_repo(payload)
    return CreateAdminResponse(msg=CREATED_SUCCESSFULLY, data=data)
  
  async def logout_admin(self, payload: LogoutAdminReqBody) -> LogoutAdminResponse:
    refresh_token = payload.refresh_token
    check_refresh_token = await self.__validate_refresh_token(refresh_token)
    if not check_refresh_token:
      raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=ERROR_TOKEN_INVALID)
    await self.db.refresh_token.delete_one({"token": refresh_token})
    return LogoutAdminResponse(msg=LOGOUT_SUCCESSFULLY)
  
  async def list_admin(self, payload: ListAdminReqQuery, request: Request) -> ListAdminResponse:
    ma_admin = request.state.decode_authorization.get("ma_admin")
    data = await self.admin_repo.list_admin_repo(payload, ma_admin)
    return ListAdminResponse(msg=GET_ADMIN_SUCCESSFULLY, data=data)
  
  async def update_admin(self, payload: UpdateAdminReqBody) -> UpdateAdminResponse:
    if payload.ngay_sinh:
      if isinstance(payload.ngay_sinh, str):
        try:
          payload.ngay_sinh = datetime.fromisoformat(payload.ngay_sinh)
        except ValueError:
          payload.ngay_sinh = datetime.strptime(payload.ngay_sinh, "%Y-%m-%d").replace(tzinfo=timezone.utc)
      elif isinstance(payload.ngay_sinh, datetime):
        pass
    payload.ngay_cap_nhat_tai_khoan = datetime.now(timezone.utc)
    row = await self.db.admin.find_one({"_id": payload.id})
    if not row:
      raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=ERROR_DATA_NOT_FOUND)
    result = await self.admin_repo.update_admin_repo(payload)
    return UpdateAdminResponse(msg=UPDATED_SUCCESSFULLY, data=result)
  
  async def detail_admin(self, params:DetailAdminReqParams) -> DetailAdminRespone:
    id = params.id
    if not ObjectId.is_valid(id):
      raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=ERROR_ID_INVALID)
    admin = await self.db.admin.find_one({"_id": ObjectId(id)})
    if not admin:
      raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=ERROR_DATA_NOT_FOUND)
    result = serialize_admin(admin)
    return DetailAdminRespone(msg=GET_ADMIN_SUCCESSFULLY, data=result)
  
  async def delete_one_admin(self, payload:DeleteOneAdminReqBody) -> DeleteOneAdminRespone:
    id = payload.id
    if not ObjectId.is_valid(id):
      raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=ERROR_ID_INVALID)
    admin = await self.db.admin.find_one({"_id": ObjectId(id)})
    if not admin:
      raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=ERROR_DATA_NOT_FOUND)
    await self.db.admin.delete_one({"_id": ObjectId(id)})
    return DeleteOneAdminRespone(msg=DELETE_SUCCESSFULLY)
  
  async def delete_many_admin(self, payload: DeleteManyAdminReqBody)->DeleteManyAdminRespone:
    object_ids = [ObjectId(id) for id in payload.ids]
    await self.db.admin.delete_many({"_id": {"$in": object_ids}})
    return DeleteManyAdminRespone(msg=DELETE_SUCCESSFULLY)

  async def refresh_token_admin(self, payload: RefreshTokenReqBody) -> RefreshTokenResponse:
    refresh_token = payload.refresh_token
    check_refresh_token = await self.__validate_refresh_token(refresh_token)
    if not check_refresh_token:
      raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=ERROR_TOKEN_INVALID)
    decode_refresh_token: TokenPayload = verify_token(refresh_token, config.REFRESH_TOKEN_SECRET_KEY)
    payload_token: RefreshTokenReqPayload = {"ma_admin": decode_refresh_token["ma_admin"], "trang_thai": decode_refresh_token["trang_thai"], "thoi_gian_het_han": decode_refresh_token["thoi_gian_het_han"]}
    result = await self.admin_repo.refresh_token_repo(payload_token)
    return RefreshTokenResponse(msg=REFRESH_TOKEN_SUCCESSFULLY, data=result)
  
  async def upload_images(self, files: List[UploadFile])->UploadImagesResponse:
    ALLOWED_EXTENSIONS = self.allowed_extensions
    MAX_FILE_SIZE = self.max_file_size_upload_img
    UPLOAD_DIR = self.upload_dir
    uploaded_files = []
    for file in files:
      ext = Path(file.filename).suffix.lower()
      if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"File {file.filename} không hợp lệ")
      contents = await file.read()
      if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"File {file.filename} vượt quá {MAX_FILE_SIZE//1024//1024}MB")
      filename = f"{uuid.uuid4()}{ext}"
      save_path = UPLOAD_DIR / filename
      with save_path.open("wb") as f:
        f.write(contents)
      uploaded_files.append({
        "filename": filename,
        "http": config.SERVER_URL,
        "upload_folder": UPLOAD_IMAGES_DIR
      })
    return UploadImagesResponse(msg=UPLOAD_SUCCESSFULLY, data=uploaded_files)
