from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.patch import ServerPatch
from app.schemas.patch import PatchCreate, PatchUpdate

class CRUDPatch(CRUDBase[ServerPatch, PatchCreate, PatchUpdate]):
    def get_by_server(self, db: Session, *, server_id: int) -> List[ServerPatch]:
        return db.query(ServerPatch).filter(ServerPatch.server_id == server_id).all()

    def get_by_status(self, db: Session, *, status: str) -> List[ServerPatch]:
        return db.query(ServerPatch).filter(ServerPatch.patch_status == status).all()

    def get_by_type(self, db: Session, *, patch_type: str) -> List[ServerPatch]:
        return db.query(ServerPatch).filter(ServerPatch.patch_type == patch_type).all()

    def get_pending_patches(self, db: Session) -> List[ServerPatch]:
        return db.query(ServerPatch).filter(ServerPatch.patch_status == "pending").all()

    def get_installed_patches(self, db: Session) -> List[ServerPatch]:
        return db.query(ServerPatch).filter(ServerPatch.patch_status == "installed").all()

    def get_failed_patches(self, db: Session) -> List[ServerPatch]:
        return db.query(ServerPatch).filter(ServerPatch.patch_status == "failed").all()

    def get_server(self, db: Session, *, id: int) -> Optional[Any]:
        from app.models.server import Server
        return db.query(Server).filter(Server.id == id).first()

crud_patch = CRUDPatch(ServerPatch) 