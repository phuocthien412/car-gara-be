from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class AdminResponseDict(BaseModel):
  id: str = Field(default_factory=str, alias="_id")
  email: str
  trang_thai: str
  name: Optional[str] = None
  sdt: Optional[str] = None
  vai_tro: Optional[str] = None
  ngay_sinh: Optional[datetime] = None
  ngay_tao_tai_khoan: Optional[datetime] = None
  ngay_cap_nhat_tai_khoan: Optional[datetime] = None

class ListAdminResponsePagination(BaseModel):
  data: List[AdminResponseDict]
  page: int
  limit: int
  total_pages: int

class ListAdminResponse(BaseModel):
  msg: str
  data: ListAdminResponsePagination

class LoginAdminResponseDict(BaseModel):
  access_token: str
  refresh_token: str
  expires_access_token: int
  expires_refresh_token: int
  admin: AdminResponseDict

class CreateAdminResponse(BaseModel):
  msg: str
  data: AdminResponseDict

class UpdateAdminResponse(CreateAdminResponse):
  pass

class LoginAdminResponse(BaseModel):
  msg: str
  data: LoginAdminResponseDict

class RefreshTokenResponse(LoginAdminResponse):
  pass

class DeleteOneAdminRespone(BaseModel):
  msg: str
  
class DeleteManyAdminRespone(DeleteOneAdminRespone):
  pass

class LogoutAdminResponse(DeleteOneAdminRespone):
  pass
  
class DetailAdminRespone(BaseModel):
  msg: str
  data: AdminResponseDict

class UploadedFileInfo(BaseModel):
  filename: str
  http: str
  upload_folder: str

class UploadImagesResponse(BaseModel):
  msg: str
  data: List[UploadedFileInfo]