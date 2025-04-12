from typing import Optional
from pydantic import BaseModel

class ReportBase(BaseModel):
    title: str
    report_type: str
    format: str
    parameters: Optional[dict] = None
    file_path: Optional[str] = None

class ReportCreate(ReportBase):
    pass

class ReportUpdate(ReportBase):
    title: Optional[str] = None
    report_type: Optional[str] = None
    format: Optional[str] = None
    parameters: Optional[dict] = None
    file_path: Optional[str] = None

class Report(ReportBase):
    id: int
    created_by_id: int

    class Config:
        orm_mode = True 