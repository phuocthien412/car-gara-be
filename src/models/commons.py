from bson import ObjectId
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler
from src.constants.messages import OBJECT_ID_INVALID

class PyObjectId(ObjectId):
  @classmethod
  def __get_pydantic_core_schema__(cls, _source_type, _handler: GetCoreSchemaHandler):
    return core_schema.no_info_after_validator_function(
      cls.validate,
      core_schema.str_schema()
    )

  @classmethod
  def validate(cls, value):
    if not ObjectId.is_valid(value):
      raise ValueError(OBJECT_ID_INVALID)
    return ObjectId(value)
  
  @classmethod
  def __get_pydantic_json_schema__(cls, _core_schema, _handler):
    return {"type": "string"}