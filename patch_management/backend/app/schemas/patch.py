from typing import Optional
from pydantic import BaseModel

class PatchBase(BaseModel):
    patch_name: str
    patch_version: str
    patch_type: str
    patch_status: str
    install_date: Optional[str] = None
    server_id: int

class PatchCreate(PatchBase):
    pass

class PatchUpdate(PatchBase):
    patch_name: Optional[str] = None
    patch_version: Optional[str] = None
    patch_type: Optional[str] = None
    patch_status: Optional[str] = None
    install_date: Optional[str] = None
    server_id: Optional[int] = None

class Patch(PatchBase):
    id: int

    class Config:
        orm_mode = True 