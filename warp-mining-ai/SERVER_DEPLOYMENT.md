# 🖥️ Warp Mining AI - Server Deployment Guide

**Download and Deploy Warp Mining AI on Your Server**

---

## 🚀 Quick Server Deployment

### Step 1: Connect to Your Server
```bash
# SSH into your server
ssh username@your-server-ip

# Or if using key authentication
ssh -i /path/to/your/key.pem username@your-server-ip
```

### Step 2: Install Prerequisites on Server
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.21.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group (to run docker without sudo)
sudo usermod -aG docker $USER

# Log out and back in, or run:
newgrp docker

# Install Git
sudo apt install git -y
```

### Step 3: Download Warp Mining AI
```bash
# Clone the repository
git clone https://github.com/BenjaminKaindu/warp-mining-ai.git

# Navigate to the project directory
cd warp-mining-ai

# Make scripts executable
chmod +x run-warp.sh
chmod +x deploy.sh
```

### Step 4: Start the System
```bash
# Start Warp Mining AI
./run-warp.sh
```

### Step 5: Configure Firewall (if needed)
```bash
# Allow necessary ports through firewall
sudo ufw allow 3000   # Open Web UI
sudo ufw allow 8888   # Mining Engine
sudo ufw allow 11434  # Ollama API

# Check firewall status
sudo ufw status
```

---

## 🌐 Server Access Configuration

### Option 1: Access via Server IP
Once running, access your system at:
- **Main Interface**: http://YOUR_SERVER_IP:3000
- **Mining Engine**: http://YOUR_SERVER_IP:8888
- **Ollama API**: http://YOUR_SERVER_IP:11434

### Option 2: Set up Domain (Optional)
```bash
# If you have a domain, you can set up a reverse proxy with Nginx
sudo apt install nginx -y

# Create Nginx configuration
sudo nano /etc/nginx/sites-available/warp-mining-ai
```

**Nginx Configuration Content:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /mining/ {
        proxy_pass http://localhost:8888/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/warp-mining-ai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🐳 Server-Specific Docker Commands

### System Management
```bash
# Check Docker status
sudo systemctl status docker

# Start Docker service
sudo systemctl start docker

# Enable Docker to start on boot
sudo systemctl enable docker

# Check Docker version
docker --version
docker-compose --version
```

### Resource Monitoring
```bash
# Check system resources
htop
df -h
free -h

# Monitor Docker containers
docker stats

# Check container logs
docker-compose logs -f
```

### Performance Optimization for Server
```bash
# Increase Docker memory limits (edit daemon.json)
sudo nano /etc/docker/daemon.json
```

**Add this content:**
```json
{
  "default-runtime": "runc",
  "runtimes": {
    "runc": {
      "path": "runc"
    }
  },
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "storage-driver": "overlay2"
}
```

```bash
# Restart Docker
sudo systemctl restart docker
```

---

## 🔒 Security Configuration

### Basic Security Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install fail2ban (protection against brute force)
sudo apt install fail2ban -y

# Configure UFW firewall
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 3000
sudo ufw allow 8888
sudo ufw allow 11434
```

### SSL/HTTPS Setup (Optional)
```bash
# Install Certbot for Let's Encrypt SSL
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renew certificates
sudo crontab -e
# Add this line:
# 0 12 * * * /usr/bin/certbot renew --quiet
```

---

## 📊 Server Monitoring

### Health Check Script
Create a monitoring script:
```bash
nano health-check.sh
```

**Content:**
```bash
#!/bin/bash

echo "🤖 Warp Mining AI - Server Health Check"
echo "======================================"

# Check if services are running
echo "Checking Docker containers..."
docker-compose ps

echo -e "\nChecking service endpoints..."
curl -s http://localhost:3000 > /dev/null && echo "✅ Web UI: Running" || echo "❌ Web UI: Down"
curl -s http://localhost:8888/health > /dev/null && echo "✅ Mining Engine: Running" || echo "❌ Mining Engine: Down"
curl -s http://localhost:11434/api/tags > /dev/null && echo "✅ Ollama: Running" || echo "❌ Ollama: Down"

echo -e "\nSystem Resources:"
echo "Memory Usage:"
free -h
echo -e "\nDisk Usage:"
df -h /
echo -e "\nDocker Stats:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

```bash
chmod +x health-check.sh
```

### Automated Monitoring (Optional)
```bash
# Add to crontab for regular health checks
crontab -e
# Add this line to run every 5 minutes:
# */5 * * * * /path/to/warp-mining-ai/health-check.sh >> /var/log/warp-health.log 2>&1
```

---

## 🔄 Backup and Recovery on Server

### Automated Backup Script
```bash
nano backup-warp.sh
```

**Content:**
```bash
#!/bin/bash

BACKUP_DIR="/backups/warp-mining-ai"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup project files
tar -czf "$BACKUP_DIR/warp-mining-ai-$DATE.tar.gz" /path/to/warp-mining-ai

# Backup Docker volumes
docker-compose down
tar -czf "$BACKUP_DIR/docker-volumes-$DATE.tar.gz" /var/lib/docker/volumes
docker-compose up -d

# Keep only last 7 backups
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_DIR/warp-mining-ai-$DATE.tar.gz"
```

```bash
chmod +x backup-warp.sh

# Schedule daily backups
crontab -e
# Add: 0 2 * * * /path/to/warp-mining-ai/backup-warp.sh
```

---

## 🚨 Troubleshooting on Server

### Common Server Issues

#### Port Access Issues
```bash
# Check if ports are open
netstat -tulpn | grep :3000
netstat -tulpn | grep :8888
netstat -tulpn | grep :11434

# Check firewall
sudo ufw status verbose

# Check if services are bound to all interfaces
docker-compose exec warp-mining-engine netstat -tulpn
```

#### Memory Issues
```bash
# Check memory usage
free -h
docker stats

# Increase swap space if needed
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

#### Docker Issues
```bash
# Restart Docker service
sudo systemctl restart docker

# Clean up Docker system
docker system prune -a

# Check Docker logs
sudo journalctl -u docker.service
```

---

## 🎯 Quick Server Deployment Commands

**One-liner for complete setup:**
```bash
curl -fsSL https://get.docker.com | sh && \
sudo usermod -aG docker $USER && \
sudo curl -L "https://github.com/docker/compose/releases/download/v2.21.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
sudo chmod +x /usr/local/bin/docker-compose && \
git clone https://github.com/BenjaminKaindu/warp-mining-ai.git && \
cd warp-mining-ai && \
chmod +x run-warp.sh && \
newgrp docker
```

**Then run:**
```bash
./run-warp.sh
```

---

## 📞 Server Support

### Essential Server Commands
```bash
# Start system
./run-warp.sh

# Stop system
docker-compose down

# Restart system
docker-compose restart

# View logs
docker-compose logs -f

# Check system status
docker-compose ps
./health-check.sh

# Emergency restart
sudo systemctl restart docker
docker-compose down && docker-compose up -d
```

### Remote Access
- **Web Interface**: http://YOUR_SERVER_IP:3000
- **Mining Engine**: http://YOUR_SERVER_IP:8888
- **SSH Access**: ssh username@YOUR_SERVER_IP

---

**🖥️ Server deployment complete! Your Warp Mining AI is now running on your server.**

*Access your mining AI from anywhere with your server's IP address!*
