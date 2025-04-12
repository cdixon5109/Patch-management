from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.crud.base import CRUDBase
from app.models.analytics import Analytics
from app.schemas.analytics import AnalyticsCreate, AnalyticsUpdate

class CRUDAnalytics(CRUDBase[Analytics, AnalyticsCreate, AnalyticsUpdate]):
    def get_metrics(self, db: Session, *, time_period: str) -> Dict[str, Any]:
        from app.models.patch import ServerPatch
        from app.models.server import Server
        
        now = datetime.utcnow()
        if time_period == "daily":
            start_time = now - timedelta(days=1)
        elif time_period == "weekly":
            start_time = now - timedelta(weeks=1)
        else:  # monthly
            start_time = now - timedelta(days=30)
        
        total_servers = db.query(Server).count()
        total_patches = db.query(ServerPatch).count()
        pending_patches = db.query(ServerPatch).filter(ServerPatch.patch_status == "pending").count()
        security_patches = db.query(ServerPatch).filter(ServerPatch.patch_type == "security").count()
        
        return {
            "total_servers": total_servers,
            "total_patches": total_patches,
            "pending_patches": pending_patches,
            "security_patches": security_patches,
            "compliance_rate": ((total_patches - pending_patches) / total_patches * 100) if total_patches > 0 else 0
        }

    def get_compliance_trend(self, db: Session, *, days: int) -> List[Dict[str, Any]]:
        from app.models.patch import ServerPatch
        from app.models.server import Server
        
        trend_data = []
        for i in range(days):
            date = datetime.utcnow() - timedelta(days=i)
            total_patches = db.query(ServerPatch).count()
            pending_patches = db.query(ServerPatch).filter(ServerPatch.patch_status == "pending").count()
            
            trend_data.append({
                "date": date.strftime("%Y-%m-%d"),
                "total_patches": total_patches,
                "pending_patches": pending_patches,
                "compliance_rate": ((total_patches - pending_patches) / total_patches * 100) if total_patches > 0 else 0
            })
        
        return trend_data

    def get_patch_distribution(self, db: Session) -> Dict[str, Any]:
        from app.models.patch import ServerPatch
        
        patches = db.query(ServerPatch).all()
        distribution = {
            "security": 0,
            "bugfix": 0,
            "enhancement": 0
        }
        
        for patch in patches:
            distribution[patch.patch_type] += 1
        
        return distribution

    def get_server_health(self, db: Session) -> List[Dict[str, Any]]:
        from app.models.server import Server
        from app.models.patch import ServerPatch
        
        servers = db.query(Server).all()
        health_data = []
        
        for server in servers:
            patches = db.query(ServerPatch).filter(ServerPatch.server_id == server.id).all()
            pending = len([p for p in patches if p.patch_status == "pending"])
            security = len([p for p in patches if p.patch_type == "security" and p.patch_status == "pending"])
            
            health_data.append({
                "server_id": server.id,
                "hostname": server.hostname,
                "os_type": server.os_type,
                "os_version": server.os_version,
                "last_patch_check": server.last_patch_check,
                "pending_updates": pending,
                "security_updates": security,
                "health_status": "healthy" if pending == 0 else "needs_attention"
            })
        
        return health_data

    def get_patch_installation_stats(self, db: Session) -> Dict[str, Any]:
        from app.models.patch import ServerPatch
        
        total_patches = db.query(ServerPatch).count()
        successful_installs = db.query(ServerPatch).filter(ServerPatch.patch_status == "installed").count()
        failed_installs = db.query(ServerPatch).filter(ServerPatch.patch_status == "failed").count()
        
        return {
            "total_patches": total_patches,
            "successful_installs": successful_installs,
            "failed_installs": failed_installs,
            "success_rate": (successful_installs / total_patches * 100) if total_patches > 0 else 0
        }

    def get_vulnerability_trend(self, db: Session, *, days: int) -> List[Dict[str, Any]]:
        from app.models.patch import ServerPatch
        
        trend_data = []
        for i in range(days):
            date = datetime.utcnow() - timedelta(days=i)
            security_patches = db.query(ServerPatch).filter(
                ServerPatch.patch_type == "security",
                ServerPatch.patch_status == "pending"
            ).count()
            
            trend_data.append({
                "date": date.strftime("%Y-%m-%d"),
                "security_patches": security_patches
            })
        
        return trend_data

crud_analytics = CRUDAnalytics(Analytics) 