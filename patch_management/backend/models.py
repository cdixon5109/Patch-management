from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class ServerStatus(str, enum.Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"

class PatchStatus(str, enum.Enum):
    PENDING = "pending"
    APPLIED = "applied"
    FAILED = "failed"

class PatchSeverity(str, enum.Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    servers = relationship("Server", back_populates="owner")

class Server(Base):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    ip_address = Column(String)
    status = Column(Enum(ServerStatus), default=ServerStatus.OFFLINE)
    os_type = Column(String)
    os_version = Column(String)
    last_checked = Column(DateTime, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    ssh_key = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="servers")
    patches = relationship("Patch", back_populates="server")

class Patch(Base):
    __tablename__ = "patches"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    version = Column(String)
    description = Column(String)
    severity = Column(Enum(PatchSeverity))
    status = Column(Enum(PatchStatus), default=PatchStatus.PENDING)
    release_date = Column(DateTime)
    server_id = Column(Integer, ForeignKey("servers.id"))
    applied_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    server = relationship("Server", back_populates="patches")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String)
    details = Column(String)
    ip_address = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow) 