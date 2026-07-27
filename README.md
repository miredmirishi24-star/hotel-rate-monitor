# Hotel Rate Monitor

Automated system to fetch and monitor hotel rates from multiple OTA (Online Travel Agency) sources and GDS (Global Distribution System), with daily tracking and variance analysis.

## Features

- **Multi-Source Integration**: Fetch rates from Expedia, Booking.com, Trip.com, and GDS
- **Daily Monitoring**: Track rates for 30 days continuously
- **Variance Analysis**: Calculate price differences and variance across sources
- **Google Sheets Integration**: Automatically upload data to Google Sheets
- **Excel Export**: Local export with formatting
- **Hotels Monitored**:
  - Sea Cliff Court, Dar es Salaam
  - Delta, Dar es Salaam
  - Oyster Bay Suites, Dar es Salaam
  - Coral Beach, Dar es Salaam

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add:
- Expedia Rapid API key
- Booking.com Partner API key
- Trip.com API key
- GDS API credentials
- Google Sheets spreadsheet ID

### 3. Google Sheets Setup

1. Create a service account in Google Cloud Console
2. Download credentials as JSON
3. Place in project root as `credentials.json`
4. Share your Google Sheet with the service account email

### 4. Run the Monitor

```bash
python main.py
```

## Output

### Local Excel File
- Stored in `./data/hotel_rates_YYYYMMDD_HHMMSS.xlsx`
- One sheet per hotel
- Columns: Date, Hotel, Source, Price, Currency, Availability, Timestamp

### Google Sheets
- Individual sheet for each hotel
- Real-time data updates
- Automated highlighting for variance

## Data Analysis

The system provides:

- **Min/Max Prices**: Lowest and highest rates per date
- **Average Price**: Mean rate across all sources
- **Variance**: Statistical variance of prices
- **Price Range**: Daily difference between highest and lowest rates
- **Standard Deviation**: Price volatility measure

## Scheduling

For continuous monitoring, use a task scheduler:

### Linux/Mac (cron)
```bash
0 * * * * cd /path/to/project && python main.py
```

### Windows (Task Scheduler)
Create a scheduled task to run `main.py` hourly

## API Documentation

### RateMonitor Class

```python
from rate_monitor import RateMonitor

monitor = RateMonitor()

# Fetch all rates for a hotel
rates = monitor.fetch_all_rates("Sea Cliff Court", "2026-08-01", "2026-08-02")

# Monitor daily rates for 30 days
df = monitor.monitor_daily_rates("Sea Cliff Court")

# Calculate variance
variance_df = monitor.calculate_variance(df)
```

### GoogleSheetsHandler Class

```python
from sheets_handler import GoogleSheetsHandler

sheets = GoogleSheetsHandler()

# Create sheet
sheets.create_sheet("Hotel Rates")

# Write data
data = [["Date", "Price"], ["2026-08-01", 250]]
sheets.write_data("Hotel Rates", data)

# Highlight variance cells
sheets.highlight_cells("Hotel Rates", ["A2:C5"], {"red": 1, "green": 0, "blue": 0})
```

## Troubleshooting

### API Connection Issues
- Verify API keys in `.env`
- Check internet connection
- Verify API endpoints are accessible

### Google Sheets Errors
- Ensure service account has access to spreadsheet
- Verify `credentials.json` is in project root
- Check spreadsheet ID in `.env`

### No Data Retrieved
- Check if hotel names match exactly
- Verify dates are in YYYY-MM-DD format
- Review API rate limits

## License

MIT License

## Support

For issues and feature requests, please create an issue in the repository.
