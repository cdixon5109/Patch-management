from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.schemas.patch import Patch, PatchCreate, PatchUpdate
from app.crud import crud_patch
from app.utils.ssh import create_ssh_client

router = APIRouter()

@router.get("/", response_model=List[Patch])
def read_patches(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve patches.
    """
    patches = crud_patch.get_multi(db, skip=skip, limit=limit)
    return patches

@router.post("/", response_model=Patch)
def create_patch(
    *,
    db: Session = Depends(deps.get_db),
    patch_in: PatchCreate,
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Create new patch.
    """
    patch = crud_patch.create(db, obj_in=patch_in)
    return patch

@router.put("/{patch_id}", response_model=Patch)
def update_patch(
    *,
    db: Session = Depends(deps.get_db),
    patch_id: int,
    patch_in: PatchUpdate,
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Update a patch.
    """
    patch = crud_patch.get(db, id=patch_id)
    if not patch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patch not found",
        )
    patch = crud_patch.update(db, db_obj=patch, obj_in=patch_in)
    return patch

@router.post("/{patch_id}/install")
def install_patch(
    *,
    db: Session = Depends(deps.get_db),
    patch_id: int,
    server_ids: List[int],
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Install patch on specified servers.
    """
    patch = crud_patch.get(db, id=patch_id)
    if not patch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patch not found",
        )
    
    results = []
    for server_id in server_ids:
        server = crud_patch.get_server(db, id=server_id)
        if not server:
            results.append({
                "server_id": server_id,
                "status": "failed",
                "error": "Server not found"
            })
            continue
        
        ssh_client = create_ssh_client(
            server.ip_address,
            server.group.ssh_username,
            server.group.ssh_key_path
        )
        
        if not ssh_client:
            results.append({
                "server_id": server_id,
                "status": "failed",
                "error": "Failed to connect to server"
            })
            continue
        
        try:
            result = ssh_client.install_patches([patch.patch_name])
            results.append({
                "server_id": server_id,
                "status": "success" if result["success"] else "failed",
                "output": result.get("stdout", ""),
                "error": result.get("stderr", "")
            })
        finally:
            ssh_client.disconnect()
    
    return results

@router.get("/compliance")
def get_patch_compliance(
    db: Session = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Get patch compliance status for all servers.
    """
    servers = crud_patch.get_all_servers(db)
    compliance_data = []
    
    for server in servers:
        ssh_client = create_ssh_client(
            server.ip_address,
            server.group.ssh_username,
            server.group.ssh_key_path
        )
        
        if not ssh_client:
            compliance_data.append({
                "server_id": server.id,
                "hostname": server.hostname,
                "status": "unreachable",
                "details": "Failed to connect to server"
            })
            continue
        
        try:
            status = ssh_client.check_patch_status()
            compliance_data.append({
                "server_id": server.id,
                "hostname": server.hostname,
                "status": "compliant" if not status.get("available_updates") else "non-compliant",
                "details": status
            })
        finally:
            ssh_client.disconnect()
    
    return compliance_data 