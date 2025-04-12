from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
import paramiko
from . import models, auth
from .database import engine, get_db
from pydantic import BaseModel
from typing import Optional

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    role: models.UserRole
    is_active: bool

    class Config:
        from_attributes = True

class ServerCreate(BaseModel):
    name: str
    ip_address: str
    os_type: str
    os_version: str
    ssh_key: str

class ServerResponse(BaseModel):
    id: int
    name: str
    ip_address: str
    status: models.ServerStatus
    os_type: str
    os_version: str
    last_checked: Optional[datetime]

    class Config:
        from_attributes = True

class PatchResponse(BaseModel):
    id: int
    name: str
    version: str
    description: str
    severity: models.PatchSeverity
    status: models.PatchStatus
    release_date: datetime
    applied_at: Optional[datetime]

    class Config:
        from_attributes = True

# Authentication endpoints
@app.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not auth.verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Server endpoints
@app.post("/servers", response_model=ServerResponse)
def create_server(
    server: ServerCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_server = models.Server(**server.dict(), owner_id=current_user.id)
    db.add(db_server)
    db.commit()
    db.refresh(db_server)
    return db_server

@app.get("/servers", response_model=List[ServerResponse])
def get_servers(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    servers = db.query(models.Server).filter(models.Server.owner_id == current_user.id).all()
    return servers

@app.get("/servers/{server_id}", response_model=ServerResponse)
def get_server(
    server_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    server = db.query(models.Server).filter(
        models.Server.id == server_id,
        models.Server.owner_id == current_user.id
    ).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return server

# Patch endpoints
@app.get("/servers/{server_id}/patches", response_model=List[PatchResponse])
def get_server_patches(
    server_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    server = db.query(models.Server).filter(
        models.Server.id == server_id,
        models.Server.owner_id == current_user.id
    ).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return server.patches

@app.post("/servers/{server_id}/patches/{patch_id}/apply")
def apply_patch(
    server_id: int,
    patch_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    server = db.query(models.Server).filter(
        models.Server.id == server_id,
        models.Server.owner_id == current_user.id
    ).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    
    patch = db.query(models.Patch).filter(
        models.Patch.id == patch_id,
        models.Patch.server_id == server_id
    ).first()
    if not patch:
        raise HTTPException(status_code=404, detail="Patch not found")
    
    try:
        # Connect to server via SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server.ip_address, username='root', key_filename=server.ssh_key)
        
        # Apply patch (example command)
        stdin, stdout, stderr = ssh.exec_command(f"yum update -y {patch.name}")
        exit_status = stdout.channel.recv_exit_status()
        
        if exit_status == 0:
            patch.status = models.PatchStatus.APPLIED
            patch.applied_at = datetime.utcnow()
        else:
            patch.status = models.PatchStatus.FAILED
        
        db.commit()
        return {"status": "success", "message": "Patch applied successfully"}
    except Exception as e:
        patch.status = models.PatchStatus.FAILED
        db.commit()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        ssh.close()

# Admin endpoints
@app.get("/admin/users", response_model=List[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    admin: models.User = Depends(auth.require_admin)
):
    return db.query(models.User).all()

@app.put("/admin/users/{user_id}/activate")
def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: models.User = Depends(auth.require_admin)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = True
    db.commit()
    return {"status": "success", "message": "User activated"} 