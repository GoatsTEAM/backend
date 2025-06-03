from pydantic import BaseModel
from typing import Optional, Dict

class MediaBase(BaseModel):
    storage_key: str
    media_type: str
    position: Optional[int] = 0
    metadata: Optional[Dict] = None

class MediaCreate(MediaBase):
    pass

class MediaInDB(MediaBase):
    media_id: int
    class Config:
        orm_mode = True
