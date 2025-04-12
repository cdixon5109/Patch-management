# Patch Management System

A comprehensive patch management system for monitoring and applying system updates across multiple servers.

## System Requirements

- Rocky Linux 9
- Python 3.9+
- Node.js 16+
- Nginx
- Let's Encrypt SSL certificate

## Deployment Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd patch_management
```

2. Make the deployment script executable:
```bash
chmod +x deploy.sh
```

3. Run the deployment script:
```bash
./deploy.sh
```

4. Follow the prompts to enter your domain name for SSL certificate generation.

## Directory Structure

```
/opt/patch_management/
├── backend/           # FastAPI backend
├── frontend/          # React frontend
└── nginx/            # Nginx configuration
```

## Service Management

- Backend service: `sudo systemctl {start|stop|restart|status} patch_management`
- Frontend service: `sudo systemctl {start|stop|restart|status} patch_management_frontend`
- Nginx service: `sudo systemctl {start|stop|restart|status} nginx`

## Logs

- Backend logs: `sudo journalctl -u patch_management`
- Frontend logs: `sudo journalctl -u patch_management_frontend`
- Nginx logs: `sudo journalctl -u nginx`

## Security Considerations

1. The application runs under a dedicated `patchman` user with limited privileges.
2. All communication is encrypted using SSL/TLS.
3. Security headers are configured in Nginx.
4. Regular updates should be applied to the system.

## Backup and Recovery

1. Database backups should be scheduled regularly.
2. Configuration files are stored in `/etc/systemd/system/` and `/etc/nginx/conf.d/`.
3. Application code is stored in `/opt/patch_management/`.

## Monitoring

- System metrics can be monitored using standard Linux tools.
- Application logs are available through journalctl.
- Nginx access and error logs are available in `/var/log/nginx/`.

## Troubleshooting

1. Check service status:
```bash
sudo systemctl status patch_management
sudo systemctl status patch_management_frontend
sudo systemctl status nginx
```

2. Check logs:
```bash
sudo journalctl -u patch_management -f
sudo journalctl -u patch_management_frontend -f
sudo journalctl -u nginx -f
```

3. Check Nginx configuration:
```bash
sudo nginx -t
```

## Support

For support, please contact the system administrator or open an issue in the repository. 