import os
import traceback
from datetime import datetime
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from src.constants.messages import ERROR_LOG_INTERNAL_SERVER_ERROR
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_500_INTERNAL_SERVER_ERROR
from src.constants.dir import LOGS_DIR

class ErrorHandler:
  def __init__(self):
    self.status_code_unprocessable_entity = HTTP_422_UNPROCESSABLE_ENTITY
    self.status_code_internal_server_error = HTTP_500_INTERNAL_SERVER_ERROR

  def error_message(self, field: str, msg: str) -> str:
    if msg == 'Field required':
      msg = f"{field.capitalize()} không được để trống"
    return msg
  
  def log_error(seft, exc: Exception, request: Request):
    today_str = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(LOGS_DIR, f"{today_str}-error.log")
    with open(log_file, "a", encoding="utf-8") as f:
      timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      f.write(f"[{timestamp}] {request.method} {request.url}\n")
      f.write(f"Error: {repr(exc)}\n")
      f.write("Traceback:\n")
      f.write("".join(traceback.format_exception(type(exc), exc, exc.__traceback__)))
      f.write("-" * 80 + "\n")

  def unprocessable_entity_error(self, request: Request, exc: RequestValidationError):
    errors = {}
    print(exc.errors())
    for err in exc.errors():
      loc = err.get("loc")
      msg = err.get("msg")
      if isinstance(msg, str) and msg.lower().startswith("value error,"):
        msg = msg.split(",", 1)[1].strip()
      if loc and len(loc) > 1:
        field = loc[1]
        errors[field] = self.error_message(field, msg)
    return JSONResponse(
      status_code=self.status_code_unprocessable_entity,
      content={"detail": errors},
    )
  
  def internal_server_error(self, request: Request, exc: Exception):
    self.log_error(exc, request)
    return JSONResponse(
      status_code=self.status_code_internal_server_error,
      content={"error": ERROR_LOG_INTERNAL_SERVER_ERROR},
    )

errorHandler = ErrorHandler()
    