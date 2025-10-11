from typing import Annotated, List
from fastapi import APIRouter, Depends, UploadFile, File, Request
from src.dto.deps_request import AuthAdminRequest, TokenPayload
from src.repository.admin import AdminRepository
from src.controllers.admin import AdminController
from src.dto.admin_respone import CreateAdminResponse, DeleteManyAdminRespone, DeleteOneAdminRespone, DetailAdminRespone, ListAdminResponse, LoginAdminResponse, LogoutAdminResponse, RefreshTokenResponse, UpdateAdminResponse, UploadImagesResponse
from src.dto.admin_request import CreateAdminReqBody, DeleteManyAdminReqBody, DeleteOneAdminReqBody, DetailAdminReqParams, ListAdminReqQuery, LoginAdminReqBody, LogoutAdminReqBody, RefreshTokenReqBody, UpdateAdminReqBody
from src.constants.path import URL_CREATE_ADMIN, URL_DELETE_ADMIN, URL_DELETE_MANY_ADMIN, URL_DETAIL_ADMIN, URL_LIST_ADMIN, URL_LOGIN_ADMIN, URL_LOGOUT_ADMIN, URL_REFRESH_TOKEN_ADMIN, URL_UPDATE_ADMIN, URL_UPLOAD_IMAGES_ADMIN

admin_router = APIRouter()
admin_repo = AdminRepository()
admin_controller = AdminController(admin_repo)
URL_DETAIL_ADMIN_WITH_ID = f"{URL_DETAIL_ADMIN}" + "/{id}"

# Description: Create account
# Path: /create
# Method: POST
# Request header: { Authorization: Bearer <access_token> }
# Body: CreateAdminReqBody
@admin_router.post(URL_CREATE_ADMIN, response_model=CreateAdminResponse)
async def create_admin(
  payload: CreateAdminReqBody, 
  _access_token_admin: Annotated[TokenPayload, Depends(AuthAdminRequest.access_token_admin)],
  _verified_admin: Annotated[None, Depends(AuthAdminRequest.verified_admin)]
  ):
  result = await admin_controller.create_admin(payload)
  return result

# Description: Login account
# Path: /login
# Method: POST
# Request header: { Authorization: Bearer <access_token> }
# Body: { email: str, password: str }
@admin_router.post(URL_LOGIN_ADMIN, response_model=LoginAdminResponse)
async def login(payload: LoginAdminReqBody):
  result = await admin_controller.login(payload)
  return result

# Description: List account with pagination and filter email, ngay_tao_tai_khoan, sort_order
# Path: /list
# Method: GET
# Request header: { Authorization: Bearer <access_token> }
# Query: { page?: int, limit?: int, email?: str, ngay_tao_tai_khoan?: str, sort_order: Literal["asc", "desc"] }
@admin_router.get(URL_LIST_ADMIN, response_model=ListAdminResponse)
async def list_admin(
    request: Request,
    _access_token_admin: Annotated[TokenPayload, Depends(AuthAdminRequest.access_token_admin)],
    _verified_admin: Annotated[None, Depends(AuthAdminRequest.verified_admin)],
    payload: ListAdminReqQuery = Depends(),
  ):
  result = await admin_controller.list_admin(payload, request)
  return result

# Description: Update account
# Path: /update
# Method: PUT
# Body: UpdateAdminReqBody
@admin_router.put(URL_UPDATE_ADMIN, response_model=UpdateAdminResponse)
async def update_admin(
    _access_token_admin: Annotated[TokenPayload, Depends(AuthAdminRequest.access_token_admin)],
    _verified_admin: Annotated[None, Depends(AuthAdminRequest.verified_admin)],
    payload: UpdateAdminReqBody
  ):
  result = await admin_controller.update_admin(payload)
  return result

# Description: Refresh token account
# Path: /refresh-token
# Method: POST
# Request Body: { refresh_token: str }
@admin_router.post(URL_REFRESH_TOKEN_ADMIN, response_model=RefreshTokenResponse)
async def refresh_token(payload: RefreshTokenReqBody):
  result = await admin_controller.refresh_token_admin(payload)
  return result

# Description: Get detail account
# Path: /detail/:id
# Method: GET
# Request header: { Authorization: Bearer <access_token> }
# Request params: { id: str }
@admin_router.get(URL_DETAIL_ADMIN_WITH_ID, response_model=DetailAdminRespone)
async def detail_admin(
  _access_token_admin: Annotated[TokenPayload, Depends(AuthAdminRequest.access_token_admin)],
  _verified_admin: Annotated[None, Depends(AuthAdminRequest.verified_admin)],
  id: str
):
  result = await admin_controller.detail_admin(params=DetailAdminReqParams(id=id))
  return result

# Description: Delete one account
# Path: /delete-one
# Method: DELETE
# Request header: { Authorization: Bearer <access_token> }
# Request body: { id: str }
@admin_router.delete(URL_DELETE_ADMIN, response_model=DeleteOneAdminRespone)
async def delete_one_admin(
  _access_token_admin: Annotated[TokenPayload, Depends(AuthAdminRequest.access_token_admin)],
  _verified_admin: Annotated[None, Depends(AuthAdminRequest.verified_admin)],
  payload:DeleteOneAdminReqBody
):
  result = await admin_controller.delete_one_admin(payload)
  return result

# Description: Delete many account
# Path: /delete-many
# Method: DELETE
# Request body: { ids: List[str] }
@admin_router.delete(URL_DELETE_MANY_ADMIN, response_model=DeleteManyAdminRespone)
async def delete_one_admin(
  _access_token_admin: Annotated[TokenPayload, Depends(AuthAdminRequest.access_token_admin)],
  _verified_admin: Annotated[None, Depends(AuthAdminRequest.verified_admin)],
  payload:DeleteManyAdminReqBody
):
  result = await admin_controller.delete_many_admin(payload)
  return result

# Description: Upload images
# Path: /upload-images
# Method: POST
# Request form data: { files: str }
@admin_router.post(URL_UPLOAD_IMAGES_ADMIN, response_model=UploadImagesResponse)
async def upload_files(files: List[UploadFile] = File(...)):
  result = await admin_controller.upload_images(files)
  return result

# Description: Logout
# Method: POST
# Path: /logout
# Request body: { refresh_token: str }
@admin_router.post(URL_LOGOUT_ADMIN, response_model=LogoutAdminResponse)
async def logout_admin(payload: LogoutAdminReqBody):
  result = await admin_controller.logout_admin(payload)
  return result