from typing import Optional
from pydantic import BaseModel

class ServerGroupBase(BaseModel):
    name: str
    description: Optional[str] = None
    ssh_username: str
    ssh_key_path: str

class ServerGroupCreate(ServerGroupBase):
    pass

class ServerGroup(ServerGroupBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class ServerBase(BaseModel):
    hostname: str
    ip_address: str
    os_type: str
    os_version: str
    is_active: bool = True
    group_id: int

class ServerCreate(ServerBase):
    pass

class ServerUpdate(ServerBase):
    hostname: Optional[str] = None
    ip_address: Optional[str] = None
    os_type: Optional[str] = None
    os_version: Optional[str] = None
    is_active: Optional[bool] = None
    group_id: Optional[int] = None

class Server(ServerBase):
    id: int
    last_patch_check: Optional[str] = None

    class Config:
        orm_mode = True 