#!/bin/bash

# Exit on error
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

print_warning() {
    echo -e "${YELLOW}[!] $1${NC}"
}

print_error() {
    echo -e "${RED}[!] $1${NC}"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "Please run as root"
    exit 1
fi

# Prompt for data preservation
read -p "Do you want to preserve the database and configuration files? (y/n): " preserve_data
if [[ $preserve_data =~ ^[Yy]$ ]]; then
    print_status "Creating backup of database and configuration..."
    BACKUP_DIR="/opt/patch_management_backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    
    # Backup database
    sudo -u postgres pg_dump patch_management > "$BACKUP_DIR/patch_management.sql"
    
    # Backup configuration files
    cp -r /opt/patch_management/backend/.env "$BACKUP_DIR/"
    cp -r /etc/nginx/ssl "$BACKUP_DIR/"
    cp -r /etc/nginx/conf.d/patch_management.conf "$BACKUP_DIR/"
    
    print_status "Backup created at $BACKUP_DIR"
fi

# Stop and disable services
print_status "Stopping and disabling services..."
systemctl stop patch_management
systemctl stop patch_scanner
systemctl disable patch_management
systemctl disable patch_scanner

# Remove systemd service files
print_status "Removing systemd service files..."
rm -f /etc/systemd/system/patch_management.service
rm -f /etc/systemd/system/patch_scanner.service
systemctl daemon-reload

# Remove Nginx configuration
print_status "Removing Nginx configuration..."
rm -f /etc/nginx/conf.d/patch_management.conf
systemctl restart nginx

# Remove application files
print_status "Removing application files..."
if [[ ! $preserve_data =~ ^[Yy]$ ]]; then
    rm -rf /opt/patch_management
else
    # Only remove non-essential files
    rm -rf /opt/patch_management/frontend
    rm -rf /opt/patch_management/backend/venv
    rm -rf /opt/patch_management/backend/__pycache__
fi

# Remove SSL certificate
print_status "Removing SSL certificate..."
certbot delete --cert-name $(hostname)

# Remove database
print_status "Removing database..."
sudo -u postgres psql -c "DROP DATABASE IF EXISTS patch_management;"
sudo -u postgres psql -c "DROP USER IF EXISTS patchman;"

# Remove application user
print_status "Removing application user..."
if id "patchman" &>/dev/null; then
    userdel -r patchman 2>/dev/null || print_warning "Could not remove patchman user home directory"
fi

# Remove installed packages (optional)
read -p "Do you want to remove installed packages? (y/n): " remove_packages
if [[ $remove_packages =~ ^[Yy]$ ]]; then
    print_status "Removing installed packages..."
    dnf remove -y nginx nodejs python3-pip postgresql-server postgresql-contrib
    dnf autoremove -y
fi

print_status "Uninstallation completed successfully!"

if [[ $preserve_data =~ ^[Yy]$ ]]; then
    print_warning "Data has been preserved in $BACKUP_DIR"
    print_warning "To restore the system, you will need to:"
    print_warning "1. Restore the database using: psql -U postgres -d patch_management -f $BACKUP_DIR/patch_management.sql"
    print_warning "2. Copy configuration files back to their original locations"
    print_warning "3. Reinstall the application using the deployment script"
fi

print_warning "Note: The following packages were not removed as they might be used by other applications:"
print_warning "- nginx"
print_warning "- nodejs"
print_warning "- python3"
print_warning "- postgresql"
print_warning "- certbot"
print_warning "If you want to remove these packages, please do so manually." 