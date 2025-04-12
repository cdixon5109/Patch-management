#!/bin/bash

# Exit on error
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Print with color
print_status() {
    echo -e "${GREEN}[*] $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}[!] $1${NC}"
}

print_error() {
    echo -e "${RED}[x] $1${NC}"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "Please run as root"
    exit 1
fi

# Check if domain name is provided
if [ -z "$1" ]; then
    print_error "Please provide domain name as argument"
    echo "Usage: ./deploy.sh <domain_name>"
    exit 1
fi

DOMAIN=$1

# System update and package installation
print_status "Updating system and installing required packages..."
dnf update -y
dnf install -y epel-release
dnf install -y nginx nodejs python3 python3-pip python3-devel gcc postgresql postgresql-server postgresql-contrib certbot python3-certbot-nginx

# Initialize PostgreSQL
print_status "Initializing PostgreSQL..."
postgresql-setup --initdb
systemctl enable postgresql
systemctl start postgresql

# Create database and user
print_status "Setting up PostgreSQL database..."
sudo -u postgres psql -c "CREATE DATABASE patch_management;"
sudo -u postgres psql -c "CREATE USER patchman WITH PASSWORD 'patchman_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE patch_management TO patchman;"

# Create application user and directories
print_status "Creating application user and directories..."
useradd -r -s /sbin/nologin patchman
mkdir -p /opt/patch_management/{backend,frontend,logs}
chown -R patchman:patchman /opt/patch_management

# Setup backend
print_status "Setting up backend..."
cd /opt/patch_management/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOL
DATABASE_URL=postgresql://patchman:patchman_password@localhost/patch_management
SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
EOL

# Setup frontend
print_status "Setting up frontend..."
cd /opt/patch_management/frontend

# Install Node.js dependencies
npm install
npm run build

# Create systemd service files
print_status "Creating systemd service files..."

# Backend service
cat > /etc/systemd/system/patch-management-backend.service << EOL
[Unit]
Description=Patch Management Backend Service
After=network.target postgresql.service

[Service]
User=patchman
Group=patchman
WorkingDirectory=/opt/patch_management/backend
Environment="PATH=/opt/patch_management/backend/venv/bin"
ExecStart=/opt/patch_management/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOL

# Frontend service
cat > /etc/systemd/system/patch-management-frontend.service << EOL
[Unit]
Description=Patch Management Frontend Service
After=network.target

[Service]
User=patchman
Group=patchman
WorkingDirectory=/opt/patch_management/frontend
ExecStart=/usr/bin/node server.js
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOL

# Patch scanner service
cat > /etc/systemd/system/patch-management-scanner.service << EOL
[Unit]
Description=Patch Management Scanner Service
After=network.target patch-management-backend.service

[Service]
User=patchman
Group=patchman
WorkingDirectory=/opt/patch_management/backend
Environment="PATH=/opt/patch_management/backend/venv/bin"
ExecStart=/opt/patch_management/backend/venv/bin/python patch_scanner.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOL

# Configure Nginx
print_status "Configuring Nginx..."
cat > /etc/nginx/conf.d/patch-management.conf << EOL
server {
    listen 80;
    server_name $DOMAIN;
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl;
    server_name $DOMAIN;

    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOL

# Get SSL certificate
print_status "Obtaining SSL certificate..."
certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN

# Enable and start services
print_status "Enabling and starting services..."
systemctl daemon-reload
systemctl enable nginx patch-management-backend patch-management-frontend patch-management-scanner
systemctl start nginx patch-management-backend patch-management-frontend patch-management-scanner

# Set up log rotation
print_status "Setting up log rotation..."
cat > /etc/logrotate.d/patch-management << EOL
/opt/patch_management/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 patchman patchman
    sharedscripts
    postrotate
        systemctl reload patch-management-backend >/dev/null 2>&1 || true
        systemctl reload patch-management-frontend >/dev/null 2>&1 || true
        systemctl reload patch-management-scanner >/dev/null 2>&1 || true
    endscript
}
EOL

print_status "Deployment completed successfully!"
print_status "The application is now accessible at https://$DOMAIN"
print_status "Default admin credentials:"
print_status "Username: admin"
print_status "Password: admin123"
print_warning "Please change the default admin password after first login!" 