from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import os

from app.api import deps
from app.schemas.report import Report, ReportCreate
from app.crud import crud_report
from app.utils.report_generator import ReportGenerator

router = APIRouter()
report_generator = ReportGenerator()

@router.get("/", response_model=List[Report])
def read_reports(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve reports.
    """
    reports = crud_report.get_multi(db, skip=skip, limit=limit)
    return reports

@router.post("/", response_model=Report)
def create_report(
    *,
    db: Session = Depends(deps.get_db),
    report_in: ReportCreate,
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Create new report.
    """
    if report_in.report_type == "compliance":
        data = crud_report.get_compliance_data(db)
        filepath = report_generator.generate_compliance_report(data)
    elif report_in.report_type == "patch_status":
        data = crud_report.get_patch_status_data(db)
        filepath = report_generator.generate_patch_status_report(data)
    elif report_in.report_type == "analytics":
        data = crud_report.get_analytics_data(db)
        filepath = report_generator.generate_analytics_report(data)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid report type",
        )
    
    report_in.file_path = filepath
    report_in.created_by_id = current_user.id
    report = crud_report.create(db, obj_in=report_in)
    return report

@router.get("/{report_id}/download")
def download_report(
    *,
    db: Session = Depends(deps.get_db),
    report_id: int,
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Download a report.
    """
    report = crud_report.get(db, id=report_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )
    
    if not os.path.exists(report.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report file not found",
        )
    
    return {
        "file_path": report.file_path,
        "content_type": "application/pdf" if report.format == "pdf" else "text/csv"
    }

@router.get("/templates")
def get_report_templates(
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Get available report templates.
    """
    return [
        {
            "type": "compliance",
            "name": "Patch Compliance Report",
            "description": "Shows patch compliance status for all servers"
        },
        {
            "type": "patch_status",
            "name": "Patch Status Report",
            "description": "Shows status of all patches across servers"
        },
        {
            "type": "analytics",
            "name": "Analytics Report",
            "description": "Shows patch management analytics and trends"
        }
    ] 