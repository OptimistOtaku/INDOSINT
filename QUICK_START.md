# 🚀 INDOSINT Quick Start Guide

Get the INDOSINT AI-Powered OSINT System up and running in minutes!

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** (version 20.10+) and **Docker Compose** (version 2.0+)
- **Node.js** (version 16+) and **npm** (version 8+)
- **Python** (version 3.9+)
- **Git** (for cloning the repository)

### Quick Installation Commands

**Ubuntu/Debian:**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Python
sudo apt-get install python3 python3-pip python3-venv
```

**macOS:**
```bash
# Install Docker Desktop
brew install --cask docker

# Install Node.js
brew install node

# Install Python
brew install python
```

**Windows:**
- Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Download and install [Node.js](https://nodejs.org/)
- Download and install [Python](https://www.python.org/downloads/)

## 🏃‍♂️ Quick Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/INDOSINT.git
cd INDOSINT
```

### 2. Run the Setup Script
```bash
# Make the script executable
chmod +x setup.sh

# Run the automated setup
./setup.sh
```

The setup script will:
- ✅ Check system requirements
- ✅ Create necessary directories
- ✅ Set up environment configuration
- ✅ Install dependencies
- ✅ Start all services
- ✅ Run health checks

### 3. Configure Environment (Optional)
```bash
# Copy the example environment file
cp env.example .env

# Edit the configuration
nano .env
```

**Important:** Update the following in your `.env` file:
- `SECRET_KEY` and `JWT_SECRET` (generate secure random strings)
- API keys for external services (optional for basic functionality)
- Database credentials if using custom databases

### 4. Access the System

Once setup is complete, access the system at:

- **🌐 Frontend**: http://localhost:3000
- **🔧 Backend API**: http://localhost:8000
- **📚 API Documentation**: http://localhost:8000/docs

## 🎯 First Steps

### 1. Create Admin Account
1. Navigate to http://localhost:3000
2. Click "Register" to create your first account
3. Use a strong password
4. Set your role as "admin" or "super_admin"

### 2. Explore the Dashboard
- **Dashboard**: Overview of system statistics and recent activity
- **Search**: Multi-modal search interface (text, voice, image, face)
- **Analysis**: Advanced analytics and behavioral analysis
- **Reports**: Generate and export investigation reports

### 3. Try Your First Search
1. Go to the Search page
2. Enter a query in any supported language
3. Select search filters and options
4. View results and analysis

## 🔧 Management Commands

### Start/Stop Services
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Restart specific service
docker-compose restart backend
```

### Database Management
```bash
# Run database migrations
docker-compose exec backend alembic upgrade head

# Create database backup
docker-compose exec postgres pg_dump -U indosint_user indosint > backup.sql

# Restore database
docker-compose exec -T postgres psql -U indosint_user indosint < backup.sql
```

### Development Commands
```bash
# Install frontend dependencies
cd frontend && npm install

# Start frontend in development mode
cd frontend && npm start

# Install backend dependencies
cd backend && pip install -r requirements.txt

# Start backend in development mode
cd backend && uvicorn app.main:app --reload
```

## 🐛 Troubleshooting

### Common Issues

**Port Already in Use:**
```bash
# Check what's using the port
sudo lsof -i :3000
sudo lsof -i :8000

# Kill the process or change ports in docker-compose.yml
```

**Database Connection Issues:**
```bash
# Check database status
docker-compose ps

# Restart database services
docker-compose restart postgres mongodb redis elasticsearch

# Check database logs
docker-compose logs postgres
```

**Memory Issues:**
```bash
# Increase Docker memory limit (Docker Desktop)
# Settings > Resources > Memory: 4GB+

# Or reduce Elasticsearch memory
# Edit docker-compose.yml: ES_JAVA_OPTS="-Xms1g -Xmx1g"
```

**Permission Issues:**
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
chmod +x setup.sh
```

### Health Checks
```bash
# Check all services
curl http://localhost:8000/health

# Check individual services
curl http://localhost:9200  # Elasticsearch
curl http://localhost:6379  # Redis
```

## 📊 Monitoring

### System Status
- **Service Health**: http://localhost:8000/health
- **Elasticsearch**: http://localhost:9200/_cluster/health
- **Redis**: `docker-compose exec redis redis-cli ping`

### Logs
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

## 🔒 Security Checklist

### Initial Security Setup
- [ ] Change default passwords in `.env`
- [ ] Configure firewall rules
- [ ] Set up SSL/TLS certificates
- [ ] Enable audit logging
- [ ] Configure backup strategy

### Production Deployment
- [ ] Use production-grade databases
- [ ] Set up monitoring and alerting
- [ ] Configure load balancing
- [ ] Implement rate limiting
- [ ] Set up automated backups

## 📚 Next Steps

### Learn More
- 📖 Read the [System Overview](docs/SYSTEM_OVERVIEW.md)
- 🔧 Check the [API Documentation](http://localhost:8000/docs)
- 🎥 Watch tutorial videos (coming soon)
- 💬 Join the community forum

### Advanced Configuration
- 🔐 Set up external authentication providers
- 🌐 Configure custom data sources
- 🤖 Fine-tune AI models
- 📊 Set up advanced analytics

### Development
- 🛠️ Contribute to the project
- 🐛 Report bugs and issues
- 💡 Suggest new features
- 📝 Improve documentation

## 🆘 Getting Help

### Support Channels
- 📧 Email: support@indosint.com
- 💬 Discord: [INDOSINT Community](https://discord.gg/indosint)
- 📖 Documentation: [docs/](docs/)
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/INDOSINT/issues)

### Emergency Contacts
- 🔥 Critical Issues: security@indosint.com
- 🚨 System Down: ops@indosint.com

---

**🎉 Congratulations!** You've successfully set up INDOSINT. Start exploring the powerful OSINT capabilities and begin your digital intelligence investigations!

**Remember:** Always use this system ethically and in compliance with applicable laws and regulations. 