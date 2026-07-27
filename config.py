import os
from dotenv import load_dotenv

load_dotenv()

# Hotel Configuration
HOTELS = {
    "Sea Cliff Court": {"id": "sea_cliff_court", "location": "Dar es Salaam"},
    "Delta": {"id": "delta", "location": "Dar es Salaam"},
    "Oyster Bay Suites": {"id": "oyster_bay_suites", "location": "Dar es Salaam"},
    "Coral Beach": {"id": "coral_beach", "location": "Dar es Salaam"},
}

# OTA Sources
SOURCES = {
    "expedia": {"name": "Expedia", "url": "https://www.expedia.com"},
    "booking": {"name": "Booking.com", "url": "https://www.booking.com"},
    "trip": {"name": "Trip.com", "url": "https://www.trip.com"},
    "gds": {"name": "GDS", "url": "https://www.gds-global.com"},
}

# API Keys and Credentials
EXPEDIA_API_KEY = os.getenv("EXPEDIA_API_KEY", "")
BOOKING_API_KEY = os.getenv("BOOKING_API_KEY", "")
TRIP_API_KEY = os.getenv("TRIP_API_KEY", "")
GDS_API_KEY = os.getenv("GDS_API_KEY", "")

# Google Sheets Configuration
GOOGLE_SHEETS_SPREADSHEET_ID = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID", "")
GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")

# Monitoring Period
MONITOR_DAYS = 30  # Monitor for 30 days
CHECK_INTERVAL = 3600  # Check every hour (in seconds)

# Output Configuration
OUTPUT_DIR = "./data"
LOG_DIR = "./logs"
SHEET_NAME = "Hotel Rates"
