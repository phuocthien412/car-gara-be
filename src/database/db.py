from motor.motor_asyncio import AsyncIOMotorClient
from src.constants.config import config
from src.constants.messages import CONNECT_DB_SUCCESSFULLY, ERROR_CONNECT_DB,SHUTDOWN_CONNECT_DB

class Database: 
  def __init__(self):
    self.client = AsyncIOMotorClient(config.DATABASE_URL)
    self.db = self.client.get_default_database()

  async def connect(self):
    try:
      await self.db.command("ping")
      print(CONNECT_DB_SUCCESSFULLY)
    except Exception as e:
      print(ERROR_CONNECT_DB, e)
      raise e
    
  async def close(self):
    if self.client:
      self.client.close()
      print(SHUTDOWN_CONNECT_DB)

  def get_collection(self, name: str):
    return self.db[name]
    
  async def index_refresh_token(self):
    self.refresh_token.create_index("token")
    self.refresh_token.create_index("thoi_gian_het_han", expireAfterSeconds=0)

  async def index_admin(self):
    self.admin.create_index("email", unique=True)
    self.admin.create_index( [("email", "text")], default_language="none",  name="email_text_index")
      
  @property
  def refresh_token(self):
    return self.db[config.COLLECTION_REFRESH_TOKEN]
  
  @property
  def admin(self):
    return self.db[config.COLLECTION_ADMIN]
  
  @property
  def dich_vu(self):
    return self.db[config.COLLECTION_DICHVU]

  @property
  def san_pham(self):
    return self.db[config.COLLECTION_SANPHAM]

  @property
  def du_an(self):
    return self.db[config.COLLECTION_DUAN]

  @property
  def tin_tuc(self):
    return self.db[config.COLLECTION_TINTUC]
  

db = Database()
