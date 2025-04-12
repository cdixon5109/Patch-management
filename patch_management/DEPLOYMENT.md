# Patch Management System Deployment Guide

This guide provides step-by-step instructions for deploying the Patch Management System on Rocky Linux 9.

## Prerequisites

- A Rocky Linux 9 server with root access
- A domain name pointing to your server's IP address
- At least 2GB RAM and 20GB disk space
- Ports 80 and 443 open in your firewall

## System Requirements

- Rocky Linux 9
- Python 3.9+
- Node.js 16+
- PostgreSQL 13+
- Nginx
- Let's Encrypt SSL certificate

## Deployment Steps

### 1. Initial Server Setup

```bash
# Update system
sudo dnf update -y

# Install required packages
sudo dnf install -y epel-release
sudo dnf install -y git
```

### 2. Clone the Repository

```bash
# Clone the repository
git clone https://github.com/your-username/patch_management.git
cd patch_management
```

### 3. Make the Deployment Script Executable

```bash
chmod +x deploy.sh
```

### 4. Run the Deployment Script

```bash
# Run the deployment script with your domain name
sudo ./deploy.sh your-domain.com
```

The script will:
1. Install all required packages
2. Set up PostgreSQL database
3. Create application directories and user
4. Configure the backend and frontend
5. Set up systemd services
6. Configure Nginx with SSL
7. Enable and start all services

### 5. Verify Installation

After deployment, verify that all services are running:

```bash
# Check service status
systemctl status nginx
systemctl status patch-management-backend
systemctl status patch-management-frontend
systemctl status patch-management-scanner
```

### 6. Access the Application

- Open your browser and navigate to `https://your-domain.com`
- Log in with the default credentials:
  - Username: admin
  - Password: admin123
- Change the default password immediately after first login

## Directory Structure

```
/opt/patch_management/
├── backend/           # Backend application files
│   ├── venv/         # Python virtual environment
│   ├── .env          # Environment variables
│   └── logs/         # Backend logs
├── frontend/         # Frontend application files
│   ├── build/        # Built frontend files
│   └── logs/         # Frontend logs
└── logs/             # Application logs
```

## Service Management

### Start Services

```bash
sudo systemctl start nginx
sudo systemctl start patch-management-backend
sudo systemctl start patch-management-frontend
sudo systemctl start patch-management-scanner
```

### Stop Services

```bash
sudo systemctl stop nginx
sudo systemctl stop patch-management-backend
sudo systemctl stop patch-management-frontend
sudo systemctl stop patch-management-scanner
```

### Restart Services

```bash
sudo systemctl restart nginx
sudo systemctl restart patch-management-backend
sudo systemctl restart patch-management-frontend
sudo systemctl restart patch-management-scanner
```

### Check Service Status

```bash
sudo systemctl status nginx
sudo systemctl status patch-management-backend
sudo systemctl status patch-management-frontend
sudo systemctl status patch-management-scanner
```

## Logs

- Backend logs: `/opt/patch_management/backend/logs/`
- Frontend logs: `/opt/patch_management/frontend/logs/`
- Application logs: `/opt/patch_management/logs/`

## Security Considerations

1. Change default admin password after first login
2. Regularly update system packages
3. Monitor application logs for suspicious activity
4. Keep SSL certificates up to date
5. Use strong passwords for database and application users
6. Regularly backup the database

## Backup and Recovery

### Database Backup

```bash
# Create backup
pg_dump -U patchman patch_management > /opt/patch_management/backup.sql

# Restore from backup
psql -U patchman patch_management < /opt/patch_management/backup.sql
```

### Configuration Backup

```bash
# Backup configuration files
tar -czf /opt/patch_management/config_backup.tar.gz \
    /opt/patch_management/backend/.env \
    /etc/nginx/conf.d/patch-management.conf \
    /etc/systemd/system/patch-management-*.service
```

## Monitoring

### System Resources

```bash
# Check system resources
htop
df -h
free -m
```

### Application Health

```bash
# Check application health
curl https://your-domain.com/api/health
```

## Troubleshooting

### Common Issues

1. **Service not starting**
   - Check service status: `systemctl status <service-name>`
   - Check logs: `journalctl -u <service-name>`

2. **Database connection issues**
   - Verify PostgreSQL is running: `systemctl status postgresql`
   - Check connection: `psql -U patchman -d patch_management`

3. **SSL certificate issues**
   - Check certificate status: `certbot certificates`
   - Renew certificate: `certbot renew`

4. **Nginx configuration issues**
   - Test configuration: `nginx -t`
   - Check error logs: `tail -f /var/log/nginx/error.log`

### Log Files

- Nginx logs: `/var/log/nginx/`
- System logs: `/var/log/messages`
- Application logs: `/opt/patch_management/logs/`

## Support

For issues and support:
1. Check the logs for error messages
2. Review the troubleshooting section
3. Open an issue on the GitHub repository
4. Contact the development team

## Updates

To update the application:

```bash
# Pull latest changes
cd /opt/patch_management
git pull

# Update backend
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Update frontend
cd ../frontend
npm install
npm run build

# Restart services
sudo systemctl restart patch-management-backend
sudo systemctl restart patch-management-frontend
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 