from jose import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from jwt import InvalidTokenError
from src.constants.config import config
from src.constants.messages import ERROR_TOKEN_INVALID, ERROR_TOKEN_EXPIRED_IN
from starlette.status import HTTP_401_UNAUTHORIZED

async def sign_token(data: dict, secret_key: str, **rest) -> str:
  to_encode = data.copy()
  now = datetime.now(timezone.utc)
  expire = datetime.now(timezone.utc) + timedelta(seconds=rest.get("thoi_gian_het_han"))
  to_encode.update(
    {
      "thoi_gian_tao": int(now.timestamp()),
      "thoi_gian_het_han": int(expire.timestamp())
    }
  )
  return jwt.encode(to_encode, secret_key, algorithm=config.ALGORITHM)
  

def verify_token(token: str, secret_key: str) -> dict:
  try:
    payload = jwt.decode(token, secret_key, algorithms=[config.ALGORITHM], options={"verify_exp": False})
    exp = payload.get("thoi_gian_het_han")
    if exp and datetime.now(timezone.utc).timestamp() > exp:
      raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail=ERROR_TOKEN_EXPIRED_IN
      )
    return payload
  except InvalidTokenError:
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=ERROR_TOKEN_INVALID)