from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.api import deps
from app.schemas.analytics import Analytics
from app.crud import crud_analytics

router = APIRouter()

@router.get("/metrics")
def get_metrics(
    db: Session = Depends(deps.get_db),
    time_period: str = "daily",
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Get patch management metrics.
    """
    if time_period not in ["daily", "weekly", "monthly"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid time period. Must be daily, weekly, or monthly",
        )
    
    metrics = crud_analytics.get_metrics(db, time_period=time_period)
    return metrics

@router.get("/compliance-trend")
def get_compliance_trend(
    db: Session = Depends(deps.get_db),
    days: int = 30,
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Get patch compliance trend over time.
    """
    if days < 1 or days > 365:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Days must be between 1 and 365",
        )
    
    trend_data = crud_analytics.get_compliance_trend(db, days=days)
    return trend_data

@router.get("/patch-distribution")
def get_patch_distribution(
    db: Session = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Get distribution of patch types.
    """
    distribution = crud_analytics.get_patch_distribution(db)
    return distribution

@router.get("/server-health")
def get_server_health(
    db: Session = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Get server health metrics.
    """
    health_data = crud_analytics.get_server_health(db)
    return health_data

@router.get("/patch-installation-stats")
def get_patch_installation_stats(
    db: Session = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Get patch installation statistics.
    """
    stats = crud_analytics.get_patch_installation_stats(db)
    return stats

@router.get("/vulnerability-trend")
def get_vulnerability_trend(
    db: Session = Depends(deps.get_db),
    days: int = 30,
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Get vulnerability trend over time.
    """
    if days < 1 or days > 365:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Days must be between 1 and 365",
        )
    
    trend_data = crud_analytics.get_vulnerability_trend(db, days=days)
    return trend_data 