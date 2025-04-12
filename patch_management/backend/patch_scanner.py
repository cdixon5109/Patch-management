import paramiko
from sqlalchemy.orm import Session
from datetime import datetime
import time
import logging
from . import models
from .database import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scan_server_patches(server: models.Server):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server.ip_address, username='root', key_filename=server.ssh_key)
        
        # Get available updates
        stdin, stdout, stderr = ssh.exec_command("yum check-update")
        updates = stdout.read().decode().split('\n')
        
        # Parse updates and create patch records
        patches = []
        for update in updates:
            if update.strip():
                name, version, _ = update.split()
                patches.append({
                    'name': name,
                    'version': version,
                    'severity': determine_severity(name),  # Implement this based on your criteria
                    'release_date': datetime.utcnow(),
                    'server_id': server.id
                })
        
        return patches
    except Exception as e:
        logger.error(f"Error scanning server {server.name}: {str(e)}")
        return []
    finally:
        ssh.close()

def determine_severity(package_name: str) -> models.PatchSeverity:
    # Implement your logic to determine patch severity
    # This is a simple example
    critical_packages = ['kernel', 'openssl', 'systemd']
    high_packages = ['nginx', 'apache', 'mysql']
    
    if package_name in critical_packages:
        return models.PatchSeverity.CRITICAL
    elif package_name in high_packages:
        return models.PatchSeverity.HIGH
    else:
        return models.PatchSeverity.MEDIUM

def update_server_status(server: models.Server, db: Session):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server.ip_address, username='root', key_filename=server.ssh_key)
        server.status = models.ServerStatus.ONLINE
    except Exception:
        server.status = models.ServerStatus.OFFLINE
    finally:
        server.last_checked = datetime.utcnow()
        db.commit()
        ssh.close()

def scan_all_servers():
    db = SessionLocal()
    try:
        servers = db.query(models.Server).all()
        for server in servers:
            # Update server status
            update_server_status(server, db)
            
            if server.status == models.ServerStatus.ONLINE:
                # Scan for patches
                patches = scan_server_patches(server)
                
                # Update or create patch records
                for patch_data in patches:
                    existing_patch = db.query(models.Patch).filter(
                        models.Patch.name == patch_data['name'],
                        models.Patch.server_id == server.id
                    ).first()
                    
                    if existing_patch:
                        if existing_patch.version != patch_data['version']:
                            existing_patch.version = patch_data['version']
                            existing_patch.status = models.PatchStatus.PENDING
                    else:
                        new_patch = models.Patch(**patch_data)
                        db.add(new_patch)
                
                db.commit()
    except Exception as e:
        logger.error(f"Error in scan_all_servers: {str(e)}")
    finally:
        db.close()

def run_scanner():
    while True:
        try:
            scan_all_servers()
            time.sleep(3600)  # Scan every hour
        except Exception as e:
            logger.error(f"Error in scanner main loop: {str(e)}")
            time.sleep(300)  # Wait 5 minutes before retrying

if __name__ == "__main__":
    run_scanner() 