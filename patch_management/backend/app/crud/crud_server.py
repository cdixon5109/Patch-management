from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.server import Server, ServerGroup
from app.schemas.server import ServerCreate, ServerUpdate, ServerGroupCreate

class CRUDServer(CRUDBase[Server, ServerCreate, ServerUpdate]):
    def get_by_hostname(self, db: Session, *, hostname: str) -> Optional[Server]:
        return db.query(Server).filter(Server.hostname == hostname).first()

    def get_by_ip(self, db: Session, *, ip_address: str) -> Optional[Server]:
        return db.query(Server).filter(Server.ip_address == ip_address).first()

    def get_by_group(self, db: Session, *, group_id: int) -> List[Server]:
        return db.query(Server).filter(Server.group_id == group_id).all()

    def get_all_servers(self, db: Session) -> List[Server]:
        return db.query(Server).all()

class CRUDServerGroup(CRUDBase[ServerGroup, ServerGroupCreate, ServerGroupCreate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[ServerGroup]:
        return db.query(ServerGroup).filter(ServerGroup.name == name).first()

    def get_by_owner(self, db: Session, *, owner_id: int) -> List[ServerGroup]:
        return db.query(ServerGroup).filter(ServerGroup.owner_id == owner_id).all()

    def create_group(
        self, db: Session, *, obj_in: ServerGroupCreate, owner_id: int
    ) -> ServerGroup:
        obj_in_data = obj_in.dict()
        obj_in_data["owner_id"] = owner_id
        db_obj = ServerGroup(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

crud_server = CRUDServer(Server)
crud_server_group = CRUDServerGroup(ServerGroup) 