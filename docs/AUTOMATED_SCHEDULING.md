# ⏱️ AUTOMATED SCHEDULING GUIDE

Set up automatic monitoring to run continuously on a schedule (hourly, daily, etc.).

## Options

1. **Docker** (Recommended) - Runs continuously
2. **Cron** (Linux/macOS) - Runs on schedule
3. **Windows Task Scheduler** - Runs on schedule
4. **Python Scheduler** - Runs in background process

---

## Option 1: Docker (Recommended - Already Configured)

### How It Works
- Container runs main.py automatically
- Repeats based on CHECK_INTERVAL in config.py (default: 3600 seconds = 1 hour)
- Auto-restarts if it crashes
- Runs 24/7

### Start It
```bash
docker-compose up -d
```

### View Execution
```bash
docker-compose logs -f
```

### Stop It
```bash
docker-compose down
```

✅ **No additional setup needed**

---

## Option 2: Cron Scheduling (Linux/macOS)

### How It Works
- Runs at specified times
- Built-in to Linux/macOS
- No separate process needed
- Emails results (optional)

### 2.1 Edit Crontab
```bash
crontab -e
```

### 2.2 Add Schedule

Add one of these lines (replace `/path/to/` with your actual path):

**Run every hour**:
```bash
0 * * * * cd /path/to/hotel-rate-monitor && /path/to/venv/bin/python main.py >> logs/cron.log 2>&1
```

**Run every 30 minutes**:
```bash
*/30 * * * * cd /path/to/hotel-rate-monitor && /path/to/venv/bin/python main.py >> logs/cron.log 2>&1
```

**Run every 2 hours**:
```bash
0 */2 * * * cd /path/to/hotel-rate-monitor && /path/to/venv/bin/python main.py >> logs/cron.log 2>&1
```

**Run every day at 8 AM**:
```bash
0 8 * * * cd /path/to/hotel-rate-monitor && /path/to/venv/bin/python main.py >> logs/cron.log 2>&1
```

**Run every day at midnight**:
```bash
0 0 * * * cd /path/to/hotel-rate-monitor && /path/to/venv/bin/python main.py >> logs/cron.log 2>&1
```

### 2.3 Find Your Paths

**Find virtual env path**:
```bash
which python  # If venv is activated
# or
ls -la venv/bin/python
```

**Find project path**:
```bash
pwd
```

### 2.4 Verify Cron Is Working
```bash
# List your cron jobs
crontab -l

# Check logs
tail -f logs/cron.log
```

### 2.5 Troubleshooting Cron

**Check if cron ran**:
```bash
# View system cron logs
log stream --predicate 'eventMessage contains[cd] "hotel-rate-monitor"'  # macOS
grep CRON /var/log/syslog  # Linux
```

**Debug a cron job**:
```bash
# Test your command manually first
cd /path/to/hotel-rate-monitor && python main.py

# Then add to cron once working
```

**Ensure .env is loaded**:
```bash
# Add to crontab (before your job):
shell=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin

0 * * * * cd /path/to/hotel-rate-monitor && /path/to/venv/bin/python main.py >> logs/cron.log 2>&1
```

---

## Option 3: Windows Task Scheduler

### 3.1 Open Task Scheduler

1. Press `Win + R`
2. Type `taskschd.msc`
3. Press Enter

### 3.2 Create Basic Task

1. Click "Create Basic Task..." (right side)
2. **Name**: `Hotel Rate Monitor`
3. **Description**: `Fetch hotel rates and update Google Sheets`
4. Click "Next"

### 3.3 Set Trigger (Schedule)

1. Select: **Hourly** (or Daily, etc.)
2. Set start time: e.g., `8:00 AM today`
3. Set recurrence: Every `1` hour(s)
4. Click "Next"

### 3.4 Set Action (What to Run)

1. Select: **Start a program**
2. **Program/script**: `C:\path\to\venv\Scripts\python.exe`
3. **Add arguments**: `main.py`
4. **Start in**: `C:\path\to\hotel-rate-monitor`
5. Click "Next"

### 3.5 Review and Create

1. Check all settings
2. Click "Finish"

### 3.6 Verify It's Running

1. Open Task Scheduler
2. Go to "Task Scheduler Library"
3. Find "Hotel Rate Monitor"
4. Look for green checkmark and "Last Run Time"

### 3.7 Manual Test

1. Right-click the task
2. Select "Run"
3. Check logs appear in `logs/`

---

## Option 4: Python Scheduler (Background Process)

Run a Python process that schedules jobs.

### 4.1 Run in Background

```bash
python scheduler.py &
```

**Output**:
```
2026-07-27 10:00:00 - root - INFO - Scheduler started
2026-07-27 10:00:00 - root - INFO - Scheduled monitoring every 3600 seconds
```

### 4.2 Keep Running (Use nohup)

```bash
nohup python scheduler.py > logs/scheduler.log 2>&1 &
```

### 4.3 Monitor the Process

```bash
# Find process ID
ps aux | grep scheduler.py

# Kill if needed
kill <PID>
```

### 4.4 Auto-Start on System Boot

**macOS (LaunchAgent)**:

1. Create file: `~/Library/LaunchAgents/com.hotel-monitor.plist`
2. Add:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.hotel-monitor</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/venv/bin/python</string>
        <string>/path/to/hotel-rate-monitor/scheduler.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/path/to/logs/scheduler.log</string>
    <key>StandardErrorPath</key>
    <string>/path/to/logs/scheduler.error.log</string>
</dict>
</plist>
```

3. Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.hotel-monitor.plist
```

**Linux (Systemd)**:

1. Create: `/etc/systemd/system/hotel-monitor.service`
2. Add:
```ini
[Unit]
Description=Hotel Rate Monitor
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/hotel-rate-monitor
ExecStart=/path/to/venv/bin/python scheduler.py
Restart=always
RestartSec=10
StandardOutput=append:/path/to/logs/scheduler.log
StandardError=append:/path/to/logs/scheduler.error.log

[Install]
WantedBy=multi-user.target
```

3. Enable:
```bash
sudo systemctl enable hotel-monitor
sudo systemctl start hotel-monitor
```

---

## Comparison

| Method | Ease | Uptime | Best For |
|--------|------|--------|----------|
| **Docker** | ⭐⭐⭐⭐⭐ | 24/7 | Production, cloud |
| **Cron** | ⭐⭐⭐ | Reliable | Servers, Linux |
| **Task Scheduler** | ⭐⭐⭐⭐ | Reliable | Windows |
| **Python Scheduler** | ⭐⭐ | Manual | Dev, testing |

---

## Monitoring Schedules

### View All Running Jobs

```bash
# Docker
docker-compose ps

# Cron
crontab -l

# Python
ps aux | grep scheduler.py

# Windows Task Scheduler
tasklist | find "python"
```

### Check Logs

```bash
# Last 50 lines
tail -50 logs/rate_monitor.log

# Real-time
tail -f logs/rate_monitor.log

# Cron logs (macOS/Linux)
log stream --predicate 'eventMessage contains[cd] "hotel-rate-monitor"'
```

---

## 🎯 Recommended Setup

**For Production**:
```bash
docker-compose up -d
```

**For Development**:
```bash
python scheduler.py
```

**For Existing Servers**:
```bash
crontab -e
# Add hourly schedule
```

---

## ✅ Verify Everything Is Working

1. **Check logs appear**:
   ```bash
   tail -f logs/rate_monitor.log
   ```

2. **Check Excel files are created**:
   ```bash
   ls -la data/hotel_rates_*.xlsx
   ```

3. **Check Google Sheets are updated**:
   - Open your Google Sheet
   - Look for new data rows
   - Check timestamp is recent

4. **Set an alert** (optional):
   - If a job fails, email you
   - Check logs for errors

---

## 🎉 You're Scheduled!

Your hotel rate monitor will now:
- ✅ Run automatically on your schedule
- ✅ Fetch rates from all OTAs
- ✅ Update Google Sheets in real-time
- ✅ Export Excel files
- ✅ Run 24/7 without manual intervention
