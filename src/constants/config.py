from pydantic_settings import BaseSettings

class Config(BaseSettings): 
  DATABASE_URL: str
  ACCESS_TOKEN_SECRET_KEY: str
  REFRESH_TOKEN_SECRET_KEY: str
  ACCESS_TOKEN_EXPIRED_IN: int
  REFRESH_TOKEN_EXPIRED_IN: int
  ALGORITHM: str  
  COLLECTION_ADMIN: str
  COLLECTION_REFRESH_TOKEN: str
  COLLECTION_DICHVU: str
  COLLECTION_SANPHAM: str
  COLLECTION_DUAN: str
  COLLECTION_TINTUC: str
  COLLECTION_LIENHE: str
  COLLECTION_VIDEO: str
  UVICORN_RUN: str
  PORT: int
  MAX_FILE_SIZE_UPLOAD_IMG: int
  ALLOWED_IMG_EXTENSIONS:str
  CLIENT_URL: str
  SERVER_URL: str
  PASSWORD_DEFAULT: str
  class Config:
    env_file = ".env"
    extra = "ignore"
config = Config()
