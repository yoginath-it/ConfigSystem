from pydantic import BaseModel
from typing import Dict, Any

class ConfigurationBase(BaseModel):
    country_code: str
    business_name: str  # New field for business name
    data: Dict[str, Any]

class ConfigurationCreate(ConfigurationBase):
    pass

class Configuration(ConfigurationBase):
    id: int

    class Config:
        orm_mode = True
