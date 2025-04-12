from sqlalchemy import Column, String, Integer, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.db.base import BaseModel

class ServerGroup(BaseModel):
    __tablename__ = "server_groups"

    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text)
    ssh_username = Column(String, nullable=False)
    ssh_key_path = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    owner = relationship("User", back_populates="server_groups")
    servers = relationship("Server", back_populates="group")
    
    def __repr__(self):
        return f"<ServerGroup {self.name}>"

class Server(BaseModel):
    __tablename__ = "servers"

    hostname = Column(String, unique=True, index=True, nullable=False)
    ip_address = Column(String, nullable=False)
    os_type = Column(String, nullable=False)
    os_version = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    last_patch_check = Column(String)
    group_id = Column(Integer, ForeignKey("server_groups.id"))
    
    # Relationships
    group = relationship("ServerGroup", back_populates="servers")
    patches = relationship("ServerPatch", back_populates="server")
    
    def __repr__(self):
        return f"<Server {self.hostname}>"

class ServerPatch(BaseModel):
    __tablename__ = "server_patches"

    server_id = Column(Integer, ForeignKey("servers.id"))
    patch_name = Column(String, nullable=False)
    patch_version = Column(String, nullable=False)
    patch_status = Column(String, nullable=False)  # pending, installed, failed
    patch_type = Column(String, nullable=False)  # security, bugfix, enhancement
    install_date = Column(String)
    
    # Relationships
    server = relationship("Server", back_populates="patches")
    
    def __repr__(self):
        return f"<ServerPatch {self.patch_name} for server {self.server_id}>" 