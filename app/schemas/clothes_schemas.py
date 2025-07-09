from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models import SizeEnum, ColorEnum

class ClothesBase(BaseModel):
    name: str
    size: SizeEnum
    color: ColorEnum

class ClothesCreate(ClothesBase):
    pass

class ClothesResponse(ClothesBase):
    id: int
    created_at: datetime
    last_modified_at: datetime

    model_config = ConfigDict(from_attributes=True)