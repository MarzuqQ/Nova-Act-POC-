# 🐳 Docker Setup for Nova Act POC

This guide explains how to run the Nova Act POC using Docker containers.

## 🏗️ Architecture

The dockerized setup consists of:

- **vendor-portal**: Flask demo portal (port 5000)
- **nova-act-automation**: Nova Act automation service
- **nova-act-scheduler**: Optional scheduled automation service
- **shared_data**: Persistent volumes for uploads, submissions, and results

## 🚀 Quick Start

### 1. Prerequisites

- Docker and Docker Compose installed
- Nova Act API key

### 2. Setup Environment

```bash
# Copy the environment template
cp docker.env.template .env

# Edit .env and add your Nova Act API key
nano .env
```

Set your Nova Act API key:
```bash
NOVA_ACT_API_KEY=your-actual-api-key-here
```

### 3. Build and Run

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

### 4. Access the Application

- **Vendor Portal**: http://localhost:5000
- **Login Credentials**:
  - Username: `shipping_admin`
  - Password: `secure_pass123`

### 5. View Results

```bash
# Check automation results
ls -la shared_data/results/

# View logs
docker-compose logs -f nova-act-automation
```

## 📋 Usage Modes

### Mode 1: One-Time Automation

Run automation once and exit:

```bash
docker-compose up vendor-portal nova-act-automation
```

### Mode 2: Scheduled Automation

Run automation every 5 minutes:

```bash
docker-compose --profile scheduler up
```

### Mode 3: Portal Only

Run just the demo portal for manual testing:

```bash
docker-compose up vendor-portal
```

## 🔧 Configuration

### Environment Variables

All configuration is done via the `.env` file:

```bash
# Required
NOVA_ACT_API_KEY=your-api-key

# Optional Portal Credentials
PORTAL_USERNAME=shipping_admin
PORTAL_PASSWORD=secure_pass123

# Optional Automation Settings
TIMEOUT=300
```

### Custom Data Files

To use different sample data:

```bash
# Place your JSON file in sample_data/
cp my-shipment-data.json sample_data/

# Update docker-compose.yml to point to your file
DATA_FILE=/app/shared_data/sample_data/my-shipment-data.json
```

## 📊 Monitoring

### Health Checks

```bash
# Check service health
docker-compose ps

# Check specific service health
curl http://localhost:5000/api/health
```

### Logs

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f vendor-portal
docker-compose logs -f nova-act-automation

# View last 50 lines
docker-compose logs --tail=50 nova-act-automation
```

### Resource Usage

```bash
# Check resource usage
docker stats

# Check disk usage
docker system df
```

## 🗂️ Data Persistence

All data is stored in the `shared_data/` directory:

```
shared_data/
├── uploads/          # Files uploaded via the portal
├── submissions/      # Form submission data
└── results/         # Automation results
```

### Backup Data

```bash
# Create backup
tar -czf nova-act-backup-$(date +%Y%m%d).tar.gz shared_data/

# Restore backup
tar -xzf nova-act-backup-YYYYMMDD.tar.gz
```

## 🔧 Development

### Rebuild Specific Service

```bash
# Rebuild only the automation service
docker-compose build nova-act-automation

# Rebuild and restart
docker-compose up -d --build nova-act-automation
```

### Debug Mode

```bash
# Run with verbose logging
docker-compose logs -f nova-act-automation

# Run automation with different data
docker-compose run --rm nova-act-automation \
  sh -c "DATA_FILE=/app/shared_data/sample_data/nested_shipment_data.json python3 main.py"
```

### Override Configuration

```bash
# Run with custom environment
NOVA_ACT_API_KEY=different-key docker-compose up

# Run with different timeout
TIMEOUT=600 docker-compose up nova-act-automation
```

## 🐛 Troubleshooting

### Common Issues

1. **Port 5000 already in use**
   ```bash
   # Stop conflicting services (like AirPlay on macOS)
   # Or change port in docker-compose.yml:
   ports: ["5001:5000"]
   ```

2. **Nova Act API key not set**
   ```bash
   # Check environment file
   cat .env
   
   # Verify environment is loaded
   docker-compose config
   ```

3. **Automation fails to connect to portal**
   ```bash
   # Check portal health
   curl http://localhost:5000/api/health
   
   # Check network connectivity
   docker-compose exec nova-act-automation curl http://vendor-portal:5000/api/health
   ```

4. **Browser/Chromium issues**
   ```bash
   # Rebuild with fresh browser installation
   docker-compose build --no-cache nova-act-automation
   ```

### Debug Commands

```bash
# Enter container shell
docker-compose exec vendor-portal bash
docker-compose exec nova-act-automation bash

# Check container logs
docker logs nova-act-vendor-portal
docker logs nova-act-automation

# Inspect container configuration
docker inspect nova-act-vendor-portal
```

## 🧹 Cleanup

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down --volumes

# Stop and remove everything
docker-compose down --volumes --remove-orphans
```

### Clean Docker System

```bash
# Remove unused containers
docker container prune

# Remove unused images
docker image prune

# Full cleanup
docker system prune -a

# Remove project volumes
docker volume rm nova-act-poc_shared_data
```

## 🚀 Production Deployment

### Security Considerations

1. **Change default credentials**:
   ```bash
   PORTAL_USERNAME=your-secure-username
   PORTAL_PASSWORD=your-secure-password
   ```

2. **Use secrets management**:
   ```yaml
   # In docker-compose.yml
   secrets:
     nova_act_api_key:
       external: true
   ```

3. **Enable HTTPS**:
   ```yaml
   # Add reverse proxy like nginx
   ```

### Scaling

```bash
# Run multiple automation instances
docker-compose up --scale nova-act-automation=3
```

### Monitoring

```bash
# Add monitoring stack
docker-compose -f docker-compose.yml -f docker-compose.monitoring.yml up
```

## 📈 Performance Tips

1. **Use build cache**: Don't use `--no-cache` unless necessary
2. **Optimize images**: Multi-stage builds for smaller images
3. **Resource limits**: Set memory/CPU limits in docker-compose.yml
4. **Volume optimization**: Use named volumes for better performance

## 🤝 Contributing

To contribute to the Docker setup:

1. Test changes with `docker-compose build`
2. Verify all services start correctly
3. Check logs for errors
4. Update documentation as needed

---

For the main project documentation, see [README.md](README.md). 