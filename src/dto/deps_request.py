from src.constants.config import config
from typing import TypedDict
from fastapi import Request, HTTPException, Depends
from src.utils.jwt import verify_token
from starlette.status import HTTP_401_UNAUTHORIZED
from src.constants.enum import ENUM_ADMIN_ACTIVE_STATUS
from src.constants.messages import ERROR_ACCESS_TOKEN_INVALID, ERROR_ACCOUNT_NOT_VERIFIED

class TokenPayload(TypedDict):
  ma_admin: str
  trang_thai: str
  thoi_gian_tao: int
  thoi_gian_het_han: int

class RefreshTokenReqPayload(TokenPayload, total=False): 
  thoi_gian_tao: None

class TokenPayloadRepo(TypedDict): 
  ma_admin: str

class AuthAdminRequest: 
  @staticmethod
  def access_token_admin(request: Request) -> TokenPayload:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
      raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail=ERROR_ACCESS_TOKEN_INVALID
      )
    token = auth_header.split(" ")[1]
    payload: TokenPayload = verify_token(token, config.ACCESS_TOKEN_SECRET_KEY)
    request.state.decode_authorization = payload
    return payload
  
  @staticmethod
  def verified_admin(payload: TokenPayload = Depends(access_token_admin)): 
    if payload.get("trang_thai") != ENUM_ADMIN_ACTIVE_STATUS:
      raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail=ERROR_ACCOUNT_NOT_VERIFIED
      )