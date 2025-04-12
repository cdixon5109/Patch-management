from typing import Optional, Dict, Any
from pydantic import BaseModel

class AnalyticsBase(BaseModel):
    metric_name: str
    metric_type: str
    data: Dict[str, Any]
    time_period: str

class AnalyticsCreate(AnalyticsBase):
    pass

class AnalyticsUpdate(AnalyticsBase):
    metric_name: Optional[str] = None
    metric_type: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    time_period: Optional[str] = None

class Analytics(AnalyticsBase):
    id: int

    class Config:
        orm_mode = True 