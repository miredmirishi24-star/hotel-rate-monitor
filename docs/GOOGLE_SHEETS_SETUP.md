# 🔧 GOOGLE SHEETS INTEGRATION SETUP

This guide will walk you through connecting your hotel rate monitor to Google Sheets for automatic data uploads.

## Why Google Sheets?
- ✅ Real-time data updates
- ✅ Automatic sharing with team
- ✅ Built-in charts and analysis
- ✅ Mobile access
- ✅ Zero database setup

---

## Step 1: Create a Google Cloud Project

### 1.1 Open Google Cloud Console
1. Go to https://console.cloud.google.com/
2. Sign in with your Google account
3. If prompted, create a new project or select existing one

### 1.2 Create a New Project (if needed)
1. Click the dropdown at the top (next to Google Cloud)
2. Click "NEW PROJECT"
3. Name it: `hotel-rate-monitor`
4. Click "CREATE"
5. Wait for creation (1-2 minutes)

### 1.3 Select Your Project
1. Click the project dropdown
2. Select your newly created project
3. Verify it's active in the top navigation

---

## Step 2: Enable Google Sheets API

### 2.1 Navigate to APIs
1. In Google Cloud Console, click "APIs & Services" → "Enabled APIs & services"
2. Click "+ ENABLE APIS AND SERVICES" (top of page)

### 2.2 Search and Enable
1. Search for: `Google Sheets API`
2. Click on it in the results
3. Click the blue "ENABLE" button
4. Wait for it to activate

### 2.3 Verify It's Enabled
1. Go to "APIs & Services" → "Enabled APIs & services"
2. You should see "Google Sheets API" in the list ✓

---

## Step 3: Create a Service Account

### 3.1 Navigate to Service Accounts
1. Go to "APIs & Services" → "Credentials"
2. Click "+ CREATE CREDENTIALS" at the top
3. Select "Service Account"

### 3.2 Fill Service Account Details
1. **Service account name**: `hotel-rate-monitor`
2. **Service account ID**: Auto-fills (keep it)
3. **Description**: `Service account for automatic hotel rate monitoring`
4. Click "CREATE AND CONTINUE"

### 3.3 Grant Permissions (Optional but Recommended)
1. **Select a role**: Search for `Editor` or `Viewer`
   - For this project, `Viewer` is sufficient
   - Or search `Google Sheets API` → select `Google Sheets API Viewer`
2. Click "CONTINUE"
3. Click "DONE"

---

## Step 4: Generate and Download JSON Key

### 4.1 Go to Service Account
1. Go to "APIs & Services" → "Credentials"
2. Under "Service Accounts", click on the one you just created
3. Click the "KEYS" tab

### 4.2 Create JSON Key
1. Click "ADD KEY" → "Create new key"
2. Select **JSON** (not P12)
3. Click "CREATE"
4. **Automatically downloads** as `<service-account-id>.json`

### 4.3 Move JSON to Your Project
```bash
# Rename and move the downloaded file
mv ~/Downloads/<service-account-id>.json ./credentials.json

# Verify it's in the right place
ls -la credentials.json
```

---

## Step 5: Create Google Sheet

### 5.1 Create a New Sheet
1. Go to https://sheets.google.com/
2. Click "+ Blank spreadsheet"
3. Name it: `Hotel Rates Monitor - Dar es Salaam`
4. This opens your new sheet

### 5.2 Get the Spreadsheet ID
1. Look at the URL:
   ```
   https://docs.google.com/spreadsheets/d/SPREADSHEET_ID_HERE/edit
   ```
2. Copy the **SPREADSHEET_ID** (long string between `/d/` and `/edit`)

### 5.3 Create Sheet Tabs (Optional but Recommended)
Prepare your sheet with tabs for each hotel:

1. Right-click the "Sheet1" tab at the bottom
2. Select "Rename"
3. Name it: `Sea Cliff Court`
4. Repeat for:
   - `Delta`
   - `Oyster Bay Suites`
   - `Coral Beach`
   - `Summary`

### 5.4 Add Headers (Optional but Recommended)
In the first tab, add column headers:

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| Date | Hotel | Source | Price | Currency | Min Price | Max Price |

---

## Step 6: Share Sheet with Service Account

### 6.1 Get Service Account Email
1. Go to Google Cloud Console → "APIs & Services" → "Credentials"
2. Click your service account
3. In the "Details" section, find **Email** (looks like: `...@...iam.gserviceaccount.com`)
4. Copy it

### 6.2 Share Your Sheet
1. Go back to your Google Sheet (https://sheets.google.com/)
2. Click "Share" (top right)
3. Paste the service account email
4. Give it **Editor** access
5. Uncheck "Notify people"
6. Click "Share"

---

## Step 7: Update .env File

### 7.1 Edit .env
```bash
nano .env
# or use your favorite editor: code .env, vim .env, etc.
```

### 7.2 Add Google Sheets Configuration
```bash
# Google Sheets Configuration
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id_here
GOOGLE_CREDENTIALS_FILE=./credentials.json
```

### 7.3 Example Complete .env
```bash
# API Keys
EXPEDIA_API_KEY=xyz123...
BOOKING_API_KEY=abc456...
TRIP_API_KEY=def789...
GDS_API_KEY=ghi012...

# Google Sheets
GOOGLE_SHEETS_SPREADSHEET_ID=1a2b3c4d5e6f7g8h9i0j
GOOGLE_CREDENTIALS_FILE=./credentials.json
```

---

## Step 8: Test the Connection

### 8.1 Run a Test
```bash
cd /path/to/hotel-rate-monitor
python -c "
from sheets_handler import GoogleSheetsHandler
sheets = GoogleSheetsHandler()
if sheets.service:
    print('✓ Google Sheets connection successful!')
else:
    print('✗ Connection failed')
"
```

### 8.2 Expected Output
```
✓ Google Sheets connection successful!
```

---

## Step 9: Run the Monitor

```bash
python main.py
```

### What Will Happen
1. Fetches rates from all 4 OTAs
2. Calculates variance
3. **Automatically creates sheets** in Google Sheets (one per hotel)
4. **Uploads data** in real-time
5. Exports Excel file to `./data/`

### Check Your Sheet
1. Refresh your Google Sheet (or go back to it)
2. You should see:
   - New sheet tabs for each hotel
   - Data with Date, Hotel, Source, Price columns
   - Real-time updates as the monitor runs

---

## 🎨 Advanced: Formatting & Highlighting

The system automatically highlights cells with high variance:

### Red Highlighting = High Price Variance
- Shows hotels with big price differences across OTAs
- Helps identify price discrepancies

### Manual Formatting (Optional)
1. Select cells with prices
2. Format → Conditional formatting
3. Add color scale: Green (low) → Red (high)
4. Drag across date range

---

## 🔄 Continuous Updates

After initial setup, data updates automatically every hour:

```bash
# Option 1: Keep running in background
python main.py &

# Option 2: Schedule with cron (Linux/Mac)
crontab -e
# Add: 0 * * * * cd /path/to/project && python main.py

# Option 3: Docker (runs continuously)
docker-compose up -d
```

---

## ✅ Troubleshooting

### "credentials.json not found"
- Verify file is in project root: `ls credentials.json`
- Check path in .env: `GOOGLE_CREDENTIALS_FILE=./credentials.json`

### "Invalid spreadsheet ID"
- Copy ID from URL again (between `/d/` and `/edit`)
- No spaces or extra characters
- Verify .env has correct ID

### "Permission denied"
- Ensure sheet is shared with service account email
- Check service account email is correct
- Give **Editor** (not Viewer) access

### "API not enabled"
- Go to Google Cloud Console
- "APIs & Services" → "Enabled APIs & services"
- Ensure "Google Sheets API" shows ✓

### "No data appearing in sheet"
- Check main.py runs without errors: `python main.py`
- Verify API keys work: `python test_fetchers.py`
- Check logs: `tail -f logs/*.log`

---

## 📊 Understanding Your Sheet

### Columns
- **Date**: Check-in date for the rate
- **Hotel**: Hotel name
- **Source**: Which OTA (Expedia, Booking, etc.)
- **Price**: Room price per night
- **Currency**: USD/TZS/etc
- **Availability**: Available or sold out
- **Timestamp**: When data was fetched

### Analysis Tab (Optional)
Add formulas for:
```
=AVERAGE(Price range)  # Average price
=MAX(Price range) - MIN(Price range)  # Price variance
=STDEV(Price range)  # Price volatility
```

---

## 🎉 You're Done!

Your hotel rate monitor is now connected to Google Sheets and will:
- ✅ Fetch rates every hour
- ✅ Upload automatically
- ✅ Show price variance
- ✅ Highlight discrepancies
- ✅ Track 30 days of history
