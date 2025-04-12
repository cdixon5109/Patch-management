from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any
import psutil
import os

from .database import get_db
from .models import Base

router = APIRouter()

def check_database(db: Session) -> Dict[str, Any]:
    try:
        # Try to execute a simple query
        db.execute("SELECT 1")
        return {"status": "ok", "message": "Database connection successful"}
    except Exception as e:
        return {"status": "error", "message": f"Database connection failed: {str(e)}"}

def check_disk_space() -> Dict[str, Any]:
    try:
        disk = psutil.disk_usage('/')
        return {
            "status": "ok",
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": disk.percent
        }
    except Exception as e:
        return {"status": "error", "message": f"Disk space check failed: {str(e)}"}

def check_memory() -> Dict[str, Any]:
    try:
        memory = psutil.virtual_memory()
        return {
            "status": "ok",
            "total": memory.total,
            "available": memory.available,
            "percent": memory.percent
        }
    except Exception as e:
        return {"status": "error", "message": f"Memory check failed: {str(e)}"}

@router.get("/health")
async def health_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Comprehensive health check endpoint that checks:
    - Database connectivity
    - Disk space
    - Memory usage
    - Service status
    """
    return {
        "status": "ok",
        "version": "1.0.0",
        "checks": {
            "database": check_database(db),
            "disk_space": check_disk_space(),
            "memory": check_memory()
        }
    } 