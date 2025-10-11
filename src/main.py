import asyncio
from fastapi import FastAPI
from starlette.requests import Request
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from src.constants.dir import UPLOAD_IMAGES_DIR
from src.error.error_handler import errorHandler
from src.routes.admin import admin_router
from src.routes.dich_vu import dichvu_router
from src.routes.san_pham import sanpham_router
from src.routes.du_an import duan_router
from src.routes.tin_tuc import tintuc_router
from src.database.db import db
from src.utils.http import start_server
from src.utils.file import init_folder
from src.constants.path import URL_ADMIN
from src.constants.tags import ADMIN_AUTH_TAG, CHART_TAG, MESSAGES_TAG, TICKETS_TAG, DICHVU_TAG, SANPHAM_TAG, DUAN_TAG, TINTUC_TAG
from src.constants.messages import SERVER_STARTING, SERVER_SHUTDOWN
from fastapi.staticfiles import StaticFiles
from pathlib import Path

UPLOAD_DIR = Path(UPLOAD_IMAGES_DIR)

init_folder()
@asynccontextmanager
async def lifespan(app: FastAPI):
  await asyncio.gather(
    db.connect(),
    db.index_refresh_token(),
    db.index_admin()
  )
  print(SERVER_STARTING)
  yield
  await db.close()
  print(SERVER_SHUTDOWN)

app = FastAPI(lifespan=lifespan)

# Add middleware
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"],
  allow_credentials=True
)
# Serve media
app.mount('/' + UPLOAD_IMAGES_DIR, StaticFiles(directory=UPLOAD_DIR), name="images")
# Handler unprocessable entity error
app.add_exception_handler(RequestValidationError, errorHandler.unprocessable_entity_error)
# Handler internal server error
@app.exception_handler(Exception)
async def internal_error_handler(request: Request, exc: Exception):
  return errorHandler.internal_server_error(request, exc)
# Add router
app.include_router(admin_router, prefix=URL_ADMIN, tags=[ADMIN_AUTH_TAG])
app.include_router(dichvu_router, prefix='/dichvu', tags=[DICHVU_TAG])
app.include_router(sanpham_router, prefix='/sanpham', tags=[SANPHAM_TAG])
app.include_router(duan_router, prefix='/duan', tags=[DUAN_TAG])
app.include_router(tintuc_router, prefix='/tintuc', tags=[TINTUC_TAG])
# Run server with certificate
if __name__ == "__main__":
  start_server()
