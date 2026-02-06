# Self-Hosted Deployment Guide

## Quick Start with Docker Compose

1. **Clone the repository:**
   ```bash
   git clone https://github.com/saltyprojects/agent-control-panel.git
   cd agent-control-panel
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env and set DB_PASSWORD to a secure value
   ```

3. **Start the application:**
   ```bash
   docker-compose up -d
   ```

4. **Access the dashboard:**
   Open http://localhost:3000/landing.html in your browser

## What's Included

- **Web server:** Node.js serving the Agent Control Panel interface
- **PostgreSQL database:** Ready for future backend implementation
- **Health checks:** Automatic container monitoring and restart
- **Persistent storage:** Database volume for data persistence

## Configuration

### Custom Port

Edit `docker-compose.yml` to change the port mapping:
```yaml
ports:
  - "8080:3000"  # Access on port 8080
```

### Custom Domain

1. Set up reverse proxy (nginx, Caddy, etc.)
2. Point to `localhost:3000`
3. Configure SSL/TLS certificates

### Database Password

**Important:** Change the default database password in `.env` before deploying:
```bash
DB_PASSWORD=your_very_secure_password_here
```

## Management Commands

### View logs:
```bash
docker-compose logs -f
```

### Stop the application:
```bash
docker-compose down
```

### Stop and remove data:
```bash
docker-compose down -v
```

### Restart after changes:
```bash
docker-compose restart
```

### Update to latest version:
```bash
git pull
docker-compose down
docker-compose build
docker-compose up -d
```

## Production Checklist

- [ ] Change default database password
- [ ] Set up SSL/TLS certificate
- [ ] Configure firewall rules
- [ ] Set up automated backups
- [ ] Enable logging/monitoring
- [ ] Review security settings

## System Requirements

- **CPU:** 1 core minimum, 2+ recommended
- **RAM:** 1GB minimum, 2GB+ recommended
- **Disk:** 5GB minimum for application and logs
- **OS:** Any Docker-compatible OS (Linux, macOS, Windows)

## Troubleshooting

### Port already in use:
```bash
# Check what's using port 3000
sudo lsof -i :3000
# Kill the process or change the port in docker-compose.yml
```

### Database connection issues:
```bash
# Check database logs
docker-compose logs db
# Restart the database
docker-compose restart db
```

### Application not responding:
```bash
# Check application logs
docker-compose logs web
# Check container health
docker-compose ps
```

## Support

For issues and questions:
- GitHub: https://github.com/saltyprojects/agent-control-panel/issues
- Documentation: See README.md

## Security

This is beta software. For production deployments:
- Use strong passwords
- Enable HTTPS
- Keep Docker and dependencies updated
- Follow security best practices
- Review the LICENSE file
