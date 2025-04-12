import paramiko
from typing import Optional, Dict, List
import os
from app.core.config import settings

class SSHClient:
    def __init__(self, hostname: str, username: str, key_path: str):
        self.hostname = hostname
        self.username = username
        self.key_path = key_path
        self.client = None

    def connect(self) -> bool:
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                hostname=self.hostname,
                username=self.username,
                key_filename=self.key_path
            )
            return True
        except Exception as e:
            print(f"SSH connection failed: {str(e)}")
            return False

    def disconnect(self):
        if self.client:
            self.client.close()

    def execute_command(self, command: str) -> Dict:
        if not self.client:
            if not self.connect():
                return {"success": False, "error": "Failed to connect to server"}

        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            exit_status = stdout.channel.recv_exit_status()
            
            return {
                "success": exit_status == 0,
                "stdout": stdout.read().decode(),
                "stderr": stderr.read().decode(),
                "exit_status": exit_status
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def check_patch_status(self) -> Dict:
        # Check for available updates
        result = self.execute_command("yum check-update")
        if not result["success"]:
            return result

        # Get installed packages
        installed = self.execute_command("rpm -qa --last")
        if not installed["success"]:
            return installed

        return {
            "success": True,
            "available_updates": result["stdout"],
            "installed_packages": installed["stdout"]
        }

    def install_patches(self, packages: List[str] = None) -> Dict:
        if packages:
            command = f"yum update -y {' '.join(packages)}"
        else:
            command = "yum update -y"

        return self.execute_command(command)

    def get_system_info(self) -> Dict:
        commands = {
            "os_release": "cat /etc/os-release",
            "kernel": "uname -r",
            "hostname": "hostname",
            "uptime": "uptime",
            "memory": "free -h",
            "disk": "df -h"
        }

        results = {}
        for key, command in commands.items():
            result = self.execute_command(command)
            if result["success"]:
                results[key] = result["stdout"]
            else:
                results[key] = f"Error: {result['error']}"

        return results

def create_ssh_client(hostname: str, username: str, key_path: str) -> Optional[SSHClient]:
    if not os.path.exists(key_path):
        return None
    
    client = SSHClient(hostname, username, key_path)
    if client.connect():
        return client
    return None 