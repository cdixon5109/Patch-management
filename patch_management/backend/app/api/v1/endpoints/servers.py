from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.schemas.server import Server, ServerCreate, ServerUpdate, ServerGroup, ServerGroupCreate
from app.crud import crud_server
from app.utils.ssh import create_ssh_client

router = APIRouter()

@router.get("/", response_model=List[Server])
def read_servers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve servers.
    """
    servers = crud_server.get_multi(db, skip=skip, limit=limit)
    return servers

@router.post("/", response_model=Server)
def create_server(
    *,
    db: Session = Depends(deps.get_db),
    server_in: ServerCreate,
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Create new server.
    """
    server = crud_server.create(db, obj_in=server_in)
    return server

@router.put("/{server_id}", response_model=Server)
def update_server(
    *,
    db: Session = Depends(deps.get_db),
    server_id: int,
    server_in: ServerUpdate,
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Update a server.
    """
    server = crud_server.get(db, id=server_id)
    if not server:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Server not found",
        )
    server = crud_server.update(db, db_obj=server, obj_in=server_in)
    return server

@router.delete("/{server_id}", response_model=Server)
def delete_server(
    *,
    db: Session = Depends(deps.get_db),
    server_id: int,
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Delete a server.
    """
    server = crud_server.get(db, id=server_id)
    if not server:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Server not found",
        )
    server = crud_server.remove(db, id=server_id)
    return server

@router.get("/{server_id}/status")
def get_server_status(
    *,
    db: Session = Depends(deps.get_db),
    server_id: int,
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Get server patch status.
    """
    server = crud_server.get(db, id=server_id)
    if not server:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Server not found",
        )
    
    ssh_client = create_ssh_client(
        server.ip_address,
        server.group.ssh_username,
        server.group.ssh_key_path
    )
    
    if not ssh_client:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to connect to server",
        )
    
    try:
        status = ssh_client.check_patch_status()
        return status
    finally:
        ssh_client.disconnect()

@router.post("/groups", response_model=ServerGroup)
def create_server_group(
    *,
    db: Session = Depends(deps.get_db),
    group_in: ServerGroupCreate,
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Create new server group.
    """
    group = crud_server.create_group(db, obj_in=group_in, owner_id=current_user.id)
    return group

@router.get("/groups", response_model=List[ServerGroup])
def read_server_groups(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve server groups.
    """
    groups = crud_server.get_groups(db, skip=skip, limit=limit)
    return groups 