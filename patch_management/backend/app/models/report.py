from sqlalchemy import Column, String, Integer, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.db.base import BaseModel

class Report(BaseModel):
    __tablename__ = "reports"

    title = Column(String, nullable=False)
    report_type = Column(String, nullable=False)  # compliance, patch_status, analytics
    format = Column(String, nullable=False)  # pdf, csv
    parameters = Column(JSON)  # Report generation parameters
    file_path = Column(String)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    created_by = relationship("User", back_populates="reports")
    
    def __repr__(self):
        return f"<Report {self.title}>"

class Analytics(BaseModel):
    __tablename__ = "analytics"

    metric_name = Column(String, nullable=False)
    metric_type = Column(String, nullable=False)  # patch_compliance, system_health, etc.
    data = Column(JSON, nullable=False)
    time_period = Column(String, nullable=False)  # daily, weekly, monthly
    
    def __repr__(self):
        return f"<Analytics {self.metric_name}>"

class PatchHistory(BaseModel):
    __tablename__ = "patch_history"

    server_id = Column(Integer, ForeignKey("servers.id"))
    patch_name = Column(String, nullable=False)
    patch_version = Column(String, nullable=False)
    action = Column(String, nullable=False)  # install, remove, update
    status = Column(String, nullable=False)  # success, failed
    details = Column(Text)
    
    def __repr__(self):
        return f"<PatchHistory {self.patch_name} on server {self.server_id}>" 