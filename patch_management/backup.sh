#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Function to print status messages
print_status() {
    echo -e "${GREEN}[*] $1${NC}"
}

print_error() {
    echo -e "${RED}[!] $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}[!] $1${NC}"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "Please run as root"
    exit 1
fi

# Create backup directory
BACKUP_DIR="/opt/patch_management/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

# Backup database
print_status "Backing up database..."
sudo -u postgres pg_dump -F c patch_management > $BACKUP_DIR/database.dump

# Backup configuration files
print_status "Backing up configuration files..."
cp -r /opt/patch_management/backend/.env $BACKUP_DIR/
cp -r /etc/nginx/conf.d/patch_management.conf $BACKUP_DIR/
cp -r /etc/systemd/system/patch_management.service $BACKUP_DIR/
cp -r /etc/systemd/system/patch_scanner.service $BACKUP_DIR/

# Backup SSH keys
print_status "Backing up SSH keys..."
cp -r /opt/patch_management/.ssh $BACKUP_DIR/

# Create archive
print_status "Creating backup archive..."
cd /opt/patch_management/backups
tar -czf $(basename $BACKUP_DIR).tar.gz $(basename $BACKUP_DIR)
rm -rf $BACKUP_DIR

# Clean up old backups (keep last 7 days)
find /opt/patch_management/backups -name "*.tar.gz" -mtime +7 -delete

print_status "Backup completed successfully!"
print_status "Backup file: /opt/patch_management/backups/$(basename $BACKUP_DIR).tar.gz" 