import re
import asyncio
from fastapi import HTTPException
from typing import cast, Tuple
from pymongo.results import DeleteResult
from bson import ObjectId
from src.dto.deps_request import RefreshTokenReqPayload, TokenPayload
from src.constants.pagination import LIMIT, PAGE
from src.database.db import db
from src.models.refresh_token import RefreshTokenModel
from src.dto.admin_respone import AdminResponseDict, ListAdminResponsePagination
from passlib.hash import bcrypt
from datetime import datetime,timedelta, timezone
from src.models.admin import AdminModel
from src.dto.admin_request import CreateAdminReqBody, LoginAdminReqRepositoryBody, ListAdminReqQuery, UpdateAdminReqBody
from src.constants.config import config
from src.utils.jwt import sign_token, verify_token
from src.constants.enum import ENUM_ADMIN_ACTIVE_STATUS, ENUM_ASC
from starlette.status import  HTTP_404_NOT_FOUND
from src.constants.messages import ERROR_DATA_NOT_FOUND
from pymongo import ASCENDING, DESCENDING
from src.utils.common import serialize_admin

class AdminRepository:
  def __init__(self):
    self.db = db

  async def __sign_access_token(self, payload: dict, expired_in: int)-> str:
    access_token = await sign_token(payload, config.ACCESS_TOKEN_SECRET_KEY, thoi_gian_het_han=expired_in)
    return access_token
  
  async def __sign_refresh_token(self, payload: dict, expired_in: int)-> str:
    refresh_token = await sign_token(payload, config.REFRESH_TOKEN_SECRET_KEY, thoi_gian_het_han=expired_in)
    return refresh_token

  def __convert_expires_access_refresh_token(self)-> tuple[datetime, datetime]:
    now = datetime.now(timezone.utc)
    expires_access_token = now + timedelta(seconds=config.ACCESS_TOKEN_EXPIRED_IN)
    expires_refresh_token = now + timedelta(seconds=config.REFRESH_TOKEN_EXPIRED_IN)
    return expires_access_token, expires_refresh_token
  
  async def login_repo(self, payload: LoginAdminReqRepositoryBody)-> dict:
    payload_dict = {"ma_admin": payload["ma_admin"], "trang_thai": payload["trang_thai"]}
    access_token, refresh_token = await asyncio.gather(
      self.__sign_access_token(payload=payload_dict, expired_in=config.ACCESS_TOKEN_EXPIRED_IN),
      self.__sign_refresh_token(payload=payload_dict, expired_in=config.REFRESH_TOKEN_EXPIRED_IN)
    )
    expires_access_token, expires_refresh_token = self.__convert_expires_access_refresh_token()
    refresh_token_data = {"token": refresh_token, "thoi_gian_het_han": expires_refresh_token, "ma_admin": payload["ma_admin"]}
    refresh_token_data = RefreshTokenModel(**refresh_token_data)
    await self.db.refresh_token.insert_one(refresh_token_data.model_dump(by_alias=True, exclude_none=True))
    result = {"access_token": access_token, "refresh_token": refresh_token, "expires_access_token": config.ACCESS_TOKEN_EXPIRED_IN, "expires_refresh_token": config.REFRESH_TOKEN_EXPIRED_IN}
    admin = await self.db.admin.find_one({"_id": ObjectId(payload["ma_admin"])})
    admin = serialize_admin(admin)
    result['admin'] = admin
    return result
  
  async def refresh_token_repo(self, payload: RefreshTokenReqPayload)-> dict:
    now = datetime.now(timezone.utc)
    payload_dict = {"ma_admin": payload["ma_admin"], "trang_thai": payload["trang_thai"]}
    new_access_token, new_refresh_token, delete_one_refresh_token = cast(
    Tuple[str, str, DeleteResult],
    await asyncio.gather(
        self.__sign_access_token(payload=payload_dict, expired_in=config.ACCESS_TOKEN_EXPIRED_IN),
        self.__sign_refresh_token(payload=payload_dict, expired_in=config.REFRESH_TOKEN_EXPIRED_IN),
        self.db.refresh_token.delete_one({"ma_admin": payload["ma_admin"]})
      )
    )
    decode_access_token: TokenPayload = verify_token(new_access_token, config.ACCESS_TOKEN_SECRET_KEY)
    decode_refresh_token: TokenPayload = verify_token(new_refresh_token, config.REFRESH_TOKEN_SECRET_KEY)
    refresh_token_data = {"token": new_refresh_token, "thoi_gian_het_han": decode_refresh_token["thoi_gian_het_han"], "ma_admin": decode_refresh_token["ma_admin"]}
    refresh_token_data = RefreshTokenModel(**refresh_token_data)
    admin, refresh_token_insert_one = await asyncio.gather(
      self.db.admin.find_one({"_id": ObjectId(payload["ma_admin"])}),
      self.db.refresh_token.insert_one(refresh_token_data.model_dump(by_alias=True, exclude_none=True))
    )
    expires_refresh_token_dt = datetime.fromtimestamp(decode_refresh_token["thoi_gian_het_han"], tz=timezone.utc)
    expires_access_token_dt = datetime.fromtimestamp(decode_access_token["thoi_gian_het_han"], tz=timezone.utc)
    expires_refresh_token = int((expires_refresh_token_dt - now).total_seconds())
    expires_access_token = int((expires_access_token_dt - now).total_seconds())
    result = {"access_token": new_access_token, "refresh_token": new_refresh_token, "expires_access_token": expires_access_token, "expires_refresh_token": expires_refresh_token}
    admin = serialize_admin(admin)
    result['admin'] = admin
    return result

  async def update_admin_repo(self, payload: UpdateAdminReqBody)->AdminResponseDict:
    data_insert = payload.model_dump(exclude_none=True, exclude={"id"})
    data = await self.db.admin.find_one_and_update({"_id": ObjectId(payload.id)}, {"$set": data_insert}, return_document=True)
    if not data:
      raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=ERROR_DATA_NOT_FOUND)
    data = serialize_admin(data)
    return data

  async def create_admin_repo(self, payload: CreateAdminReqBody)->AdminResponseDict:
    hashed_password = bcrypt.hash(config.PASSWORD_DEFAULT)
    data_obj = payload.model_dump()
    data_obj["trang_thai"] = ENUM_ADMIN_ACTIVE_STATUS
    data_obj["password"] = hashed_password
    data_schema = AdminModel(**data_obj) 
    data_dump = data_schema.model_dump(by_alias=True, exclude_none=True, exclude={"id"})
    data_insert = await self.db.admin.insert_one(data_dump)
    admin_find_one = await self.db.admin.find_one(
      {"_id": data_insert.inserted_id}, 
      {"password": 0}
    )
    if not admin_find_one:
      raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=ERROR_DATA_NOT_FOUND)
    admin_find_one = serialize_admin(admin_find_one)
    return admin_find_one
  
  async def is_exist_email(self, email: str) -> bool:
    email = await self.db.admin.find_one({"email": email})
    return email is not None
    
  async def list_admin_repo(self, payload: ListAdminReqQuery, ma_admin: str) -> ListAdminResponsePagination:
    page = int(payload.page or int(PAGE))
    limit = int(payload.limit or int(LIMIT))
    email = payload.email
    filter_query = {}
    sort_direction = DESCENDING if payload.sort_order != ENUM_ASC else ASCENDING
    filter_query["_id"] = {"$ne": ObjectId(ma_admin)}
    if email:
      filter_query["email"] = {"$regex": re.escape(email), "$options": "i"}
    skip = (page - 1) *limit
    data, total = await asyncio.gather(
      self.db.admin.find(filter_query,{"password": 0}).sort("ngay_tao_tai_khoan", sort_direction).skip(skip).limit(limit).to_list(length=None),
      self.db.admin.count_documents(filter_query)
    )
    result = [{**doc, "_id": str(doc["_id"])} for doc in data]
    return ListAdminResponsePagination(
      data=result,
      page=page,
      limit=limit,
      total_pages=(total + limit - 1) // limit
    )
    