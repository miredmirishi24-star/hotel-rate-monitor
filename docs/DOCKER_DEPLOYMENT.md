# 🐳 DOCKER DEPLOYMENT GUIDE

Deploy your hotel rate monitor as a containerized application for easy deployment and continuous monitoring.

## Benefits of Docker
- ✅ No Python installation needed on server
- ✅ Consistent environment across machines
- ✅ Easy to scale
- ✅ One-command deployment
- ✅ Runs 24/7 with auto-restart

---

## Prerequisites

### Install Docker

#### On Windows
1. Download [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. Run the installer
3. Restart your computer
4. Verify: `docker --version`

#### On macOS
```bash
brew install docker docker-compose
```

#### On Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker $USER
# Logout and login for changes to take effect
```

### Verify Installation
```bash
docker --version
docker-compose --version
```

---

## Step 1: Prepare Your Environment

### 1.1 Ensure Files Are Ready
```bash
cd /path/to/hotel-rate-monitor

# Check required files exist
ls -la Dockerfile docker-compose.yml .env
```

### 1.2 Create Data Directory
```bash
mkdir -p data logs
chmod 777 data logs
```

---

## Step 2: Build Docker Image

### 2.1 Build the Image
```bash
docker build -t hotel-rate-monitor:latest .
```

**Output** (first build takes 2-3 minutes):
```
Step 1/8 : FROM python:3.11-slim
Step 2/8 : WORKDIR /app
...
Successfully built abc123def456
Successfully tagged hotel-rate-monitor:latest
```

### 2.2 Verify Image Was Built
```bash
docker images | grep hotel-rate-monitor
```

**Output**:
```
hotel-rate-monitor   latest   abc123def456   2 minutes ago   250MB
```

---

## Step 3: Configure Docker Compose

### 3.1 Review docker-compose.yml

The file already has the correct configuration:

```yaml
version: '3.8'

services:
  rate-monitor:
    build: .
    container_name: hotel-rate-monitor
    environment:
      - EXPEDIA_API_KEY=${EXPEDIA_API_KEY}
      - BOOKING_API_KEY=${BOOKING_API_KEY}
      - TRIP_API_KEY=${TRIP_API_KEY}
      - GDS_API_KEY=${GDS_API_KEY}
      - GOOGLE_SHEETS_SPREADSHEET_ID=${GOOGLE_SHEETS_SPREADSHEET_ID}
    volumes:
      - ./data:/app/data          # Excel files
      - ./logs:/app/logs          # Log files
      - ./credentials.json:/app/credentials.json:ro  # Google auth
    restart: always              # Auto-restart on crash
    networks:
      - monitor-network

networks:
  monitor-network:
    driver: bridge
```

### 3.2 Verify .env Configuration
```bash
cat .env | grep -E "API_KEY|SPREADSHEET"
```

**Expected output**:
```
EXPEDIA_API_KEY=xyz123...
BOOKING_API_KEY=abc456...
TRIP_API_KEY=def789...
GDS_API_KEY=ghi012...
GOOGLE_SHEETS_SPREADSHEET_ID=1a2b3c...
```

---

## Step 4: Start the Container

### 4.1 Start in Background
```bash
docker-compose up -d
```

**Output**:
```
Creating hotel-rate-monitor ... done
```

### 4.2 Verify Container Is Running
```bash
docker-compose ps
```

**Output**:
```
NAME                    COMMAND              SERVICE         STATUS
hotel-rate-monitor      "python main.py"     rate-monitor    Up 5 seconds
```

### 4.3 Check Logs
```bash
docker-compose logs -f
```

**Expected output** (wait a few seconds):
```
rate-monitor | 2026-07-27 10:15:30 - rate_monitor - INFO - Fetching rates for all hotels...
rate-monitor | 2026-07-27 10:15:30 - rate_monitor - INFO - Monitoring Sea Cliff Court...
rate-monitor | 2026-07-27 10:15:35 - sheets_handler - INFO - Data written to 'Sea Cliff Court Rates'
```

---

## Step 5: Monitor Logs

### 5.1 View Recent Logs
```bash
# Last 50 lines
docker-compose logs --tail 50

# Follow real-time (Ctrl+C to exit)
docker-compose logs -f
```

### 5.2 View Local Logs
```bash
ls -la logs/
cat logs/*.log
```

---

## Step 6: Verify Data Is Being Collected

### 6.1 Check Excel Files
```bash
ls -lah data/
# You should see: hotel_rates_YYYYMMDD_HHMMSS.xlsx
```

### 6.2 Check Google Sheets
1. Go to your Google Sheet
2. Refresh (Ctrl+R or Cmd+R)
3. You should see new data tabs and rows

### 6.3 Run Container Commands
```bash
# Execute command in running container
docker-compose exec rate-monitor python -c "from config import HOTELS; print(list(HOTELS.keys()))"

# Output:
# ['Sea Cliff Court', 'Delta', 'Oyster Bay Suites', 'Coral Beach']
```

---

## Step 7: Management Commands

### 7.1 Stop the Container
```bash
docker-compose down
```

**Output**:
```
Stopping hotel-rate-monitor ... done
Removing hotel-rate-monitor ... done
```

### 7.2 Restart the Container
```bash
docker-compose restart
```

### 7.3 View Container Details
```bash
docker-compose logs --tail 100
docker stats hotel-rate-monitor
```

### 7.4 Remove Container and Image
```bash
# Stop and remove
docker-compose down

# Remove image
docker rmi hotel-rate-monitor:latest
```

---

## Step 8: Deploy to Server (Cloud)

### Option A: AWS EC2

```bash
# 1. SSH into EC2 instance
ssh -i your-key.pem ec2-user@your-ec2-ip

# 2. Install Docker
sudo yum update -y
sudo yum install -y docker
sudo systemctl start docker
sudo usermod -aG docker ec2-user

# 3. Clone your repo
git clone https://github.com/your-username/hotel-rate-monitor.git
cd hotel-rate-monitor
git checkout feature/rate-fetcher

# 4. Copy credentials and .env
# (Use scp or paste contents)

# 5. Start
docker-compose up -d
```

### Option B: Google Cloud Run

```bash
# 1. Install gcloud CLI
curl https://sdk.cloud.google.com | bash

# 2. Authenticate
gcloud auth login

# 3. Deploy
gcloud run deploy hotel-rate-monitor \
  --source . \
  --memory 512Mi \
  --timeout 3600
```

### Option C: Heroku

```bash
# 1. Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# 2. Login
heroku login

# 3. Create app
heroku create hotel-rate-monitor

# 4. Set environment variables
heroku config:set EXPEDIA_API_KEY=your_key
heroku config:set BOOKING_API_KEY=your_key
# ... set other keys

# 5. Deploy
git push heroku feature/rate-fetcher:main
```

---

## Step 9: Continuous Monitoring

### 9.1 Enable Auto-Restart
The `docker-compose.yml` already includes `restart: always`, which means:
- Container restarts if it crashes
- Container starts on Docker daemon restart
- Container keeps running indefinitely

### 9.2 Health Check (Optional)
Add to `docker-compose.yml`:

```yaml
healthcheck:
  test: ["CMD", "python", "-c", "from config import HOTELS; print(1)"]
  interval: 5m
  timeout: 10s
  retries: 3
```

### 9.3 Monitor Resource Usage
```bash
# Check CPU, Memory
docker stats hotel-rate-monitor

# Output:
CONTAINER    CPU %    MEM USAGE / LIMIT
hotel-...    0.1%     150MiB / 1GiB
```

---

## 🔄 Updating the Container

### When You Make Code Changes

```bash
# 1. Commit changes
git add .
git commit -m "feat: add new OTA source"
git push

# 2. Pull latest
git pull origin feature/rate-fetcher

# 3. Rebuild image
docker-compose down
docker build -t hotel-rate-monitor:latest .

# 4. Start again
docker-compose up -d
```

---

## ✅ Troubleshooting

### Container Won't Start
```bash
# Check error logs
docker-compose logs

# Verify .env exists
ls -la .env

# Verify credentials.json exists
ls -la credentials.json
```

### Permission Denied
```bash
# Fix file permissions
sudo chown -R $USER:$USER data logs credentials.json
chmod 644 credentials.json
```

### API Key Errors
```bash
# Verify keys are set
docker-compose exec rate-monitor python -c "import os; print(os.getenv('EXPEDIA_API_KEY'))"

# Should print your key (not empty)
```

### Container Out of Memory
```bash
# Increase memory in docker-compose.yml
mem_limit: 1g

# Or check what's using memory
docker stats
```

---

## 📊 Production Checklist

- [ ] All API keys configured
- [ ] Google Sheets sheet created and shared
- [ ] credentials.json placed in project root
- [ ] Docker image built successfully
- [ ] Container running without errors
- [ ] Data appearing in Excel files
- [ ] Data appearing in Google Sheets
- [ ] Logs being written to `./logs/`
- [ ] Auto-restart enabled
- [ ] Resource monitoring in place

---

## 🎉 You're Running!

Your hotel rate monitor is now:
- ✅ Running in Docker
- ✅ Fetching rates every hour
- ✅ Uploading to Google Sheets
- ✅ Exporting to Excel
- ✅ Auto-restarting on failure
- ✅ Ready for production
