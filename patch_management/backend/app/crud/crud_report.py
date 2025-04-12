from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.report import Report
from app.schemas.report import ReportCreate, ReportUpdate

class CRUDReport(CRUDBase[Report, ReportCreate, ReportUpdate]):
    def get_by_user(self, db: Session, *, user_id: int) -> List[Report]:
        return db.query(Report).filter(Report.created_by_id == user_id).all()

    def get_by_type(self, db: Session, *, report_type: str) -> List[Report]:
        return db.query(Report).filter(Report.report_type == report_type).all()

    def get_compliance_data(self, db: Session) -> List[Dict[str, Any]]:
        from app.models.server import Server
        from app.models.patch import ServerPatch
        
        servers = db.query(Server).all()
        compliance_data = []
        
        for server in servers:
            patches = db.query(ServerPatch).filter(ServerPatch.server_id == server.id).all()
            pending = len([p for p in patches if p.patch_status == "pending"])
            security = len([p for p in patches if p.patch_type == "security" and p.patch_status == "pending"])
            
            compliance_data.append({
                "hostname": server.hostname,
                "os_type": server.os_type,
                "os_version": server.os_version,
                "last_patch_check": server.last_patch_check,
                "pending_updates": pending,
                "security_updates": security,
                "compliance_status": "compliant" if pending == 0 else "non-compliant"
            })
        
        return compliance_data

    def get_patch_status_data(self, db: Session) -> List[Dict[str, Any]]:
        from app.models.patch import ServerPatch
        from app.models.server import Server
        
        patches = db.query(ServerPatch).all()
        patch_data = []
        
        for patch in patches:
            server = db.query(Server).filter(Server.id == patch.server_id).first()
            patch_data.append({
                "patch_name": patch.patch_name,
                "patch_version": patch.patch_version,
                "patch_type": patch.patch_type,
                "affected_servers": server.hostname if server else "Unknown",
                "status": patch.patch_status,
                "install_date": patch.install_date
            })
        
        return patch_data

    def get_analytics_data(self, db: Session) -> Dict[str, Any]:
        from app.models.patch import ServerPatch
        from app.models.server import Server
        
        total_servers = db.query(Server).count()
        total_patches = db.query(ServerPatch).count()
        pending_patches = db.query(ServerPatch).filter(ServerPatch.patch_status == "pending").count()
        security_patches = db.query(ServerPatch).filter(ServerPatch.patch_type == "security").count()
        
        return {
            "total_servers": {
                "type": "count",
                "value": total_servers,
                "period": "current"
            },
            "total_patches": {
                "type": "count",
                "value": total_patches,
                "period": "current"
            },
            "pending_patches": {
                "type": "count",
                "value": pending_patches,
                "period": "current"
            },
            "security_patches": {
                "type": "count",
                "value": security_patches,
                "period": "current"
            }
        }

crud_report = CRUDReport(Report) 