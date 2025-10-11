import httpx
import random
from bson import ObjectId
from src.constants.config import config

def serialize_admin(admin: dict) -> dict:
  if not admin:
    return {}
  admin["_id"] = str(admin["_id"])
  if "password" in admin:
    del admin["password"]
  return admin

def convert_object_id(obj):
  if isinstance(obj, ObjectId):
    return str(obj)
  elif isinstance(obj, dict):
    return {k: convert_object_id(v) for k, v in obj.items()}
  elif isinstance(obj, list):
    return [convert_object_id(i) for i in obj]
  return obj

def merge_payload(base: dict, extra: dict) -> dict:
  for key, value in extra.items():
    if value not in [None, "", [], {}]:
      base[key] = value
  return base

def generate_random_number() -> str:
  return "1" + "".join(random.choices("0123456789", k=10))
