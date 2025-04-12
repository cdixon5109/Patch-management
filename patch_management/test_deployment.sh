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

# Test PostgreSQL
print_status "Testing PostgreSQL..."
if ! systemctl is-active --quiet postgresql; then
    print_error "PostgreSQL is not running"
    exit 1
fi

# Test Nginx
print_status "Testing Nginx..."
if ! systemctl is-active --quiet nginx; then
    print_error "Nginx is not running"
    exit 1
fi

# Test backend service
print_status "Testing backend service..."
if ! systemctl is-active --quiet patch_management; then
    print_error "Backend service is not running"
    exit 1
fi

# Test patch scanner service
print_status "Testing patch scanner service..."
if ! systemctl is-active --quiet patch_scanner; then
    print_error "Patch scanner service is not running"
    exit 1
fi

# Test SSL certificate
print_status "Testing SSL certificate..."
if [ ! -f "/etc/letsencrypt/live/$(hostname)/fullchain.pem" ]; then
    print_error "SSL certificate not found"
    exit 1
fi

# Test database connection
print_status "Testing database connection..."
if ! sudo -u postgres psql -c "\l" | grep -q "patch_management"; then
    print_error "Database connection failed"
    exit 1
fi

# Test API endpoint
print_status "Testing API endpoint..."
if ! curl -s -k https://localhost/api/health | grep -q "ok"; then
    print_error "API endpoint test failed"
    exit 1
fi

# Test frontend
print_status "Testing frontend..."
if ! curl -s -k https://localhost | grep -q "Patch Management"; then
    print_error "Frontend test failed"
    exit 1
fi

print_status "All tests passed successfully!" 