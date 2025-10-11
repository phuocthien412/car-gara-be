import uvicorn
from src.constants.config import config

def start_server():
  is_production = config.IS_PRODUCTION.lower() == "true"
  if is_production:
    print(f"🚀 Starting server with HTTPS at {config.CLIENT_URL}")
    uvicorn.run(
      config.UVICORN_RUN,
      host=config.CLIENT_URL,
      reload=True
      )
  else:
    print(f"🚀 Starting server with HTTP at http://{config.HOST_NAME}:{config.PORT}")
    uvicorn.run(
      config.UVICORN_RUN,
      host=config.HOST_NAME,
      port=config.PORT,
      reload=True
    )
