from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, List
import logging
from config import HOTELS, MONITOR_DAYS
from fetchers import ExpediaFetcher, BookingFetcher, TripFetcher, GDSFetcher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RateMonitor:
    """Main rate monitoring system"""
    
    def __init__(self):
        self.fetchers = [
            ExpediaFetcher(),
            BookingFetcher(),
            TripFetcher(),
            GDSFetcher(),
        ]
        self.rates_history = []
        
    def fetch_all_rates(self, hotel_name: str, check_in: str, check_out: str) -> Dict:
        """Fetch rates from all sources for a hotel"""
        rates = {}
        
        for fetcher in self.fetchers:
            try:
                rate = fetcher.fetch_rate(hotel_name, check_in, check_out)
                if rate:
                    rates[fetcher.source_name] = rate
                    logger.info(f"{fetcher.source_name}: {hotel_name} - ${rate.get('price')}")
            except Exception as e:
                logger.error(f"Error fetching from {fetcher.source_name}: {str(e)}")
        
        return rates
    
    def monitor_daily_rates(self, hotel_name: str) -> pd.DataFrame:
        """Monitor rates for a hotel over 30 days"""
        data = []
        today = datetime.now().date()
        
        for day_offset in range(MONITOR_DAYS):
            check_in = (today + timedelta(days=day_offset)).isoformat()
            check_out = (today + timedelta(days=day_offset + 1)).isoformat()
            
            rates = self.fetch_all_rates(hotel_name, check_in, check_out)
            
            for source, rate_data in rates.items():
                data.append({
                    "Date": check_in,
                    "Hotel": hotel_name,
                    "Source": source,
                    "Price": rate_data.get("price"),
                    "Currency": rate_data.get("currency"),
                    "Availability": rate_data.get("availability"),
                    "Timestamp": rate_data.get("timestamp"),
                })
        
        df = pd.DataFrame(data)
        self.rates_history.append(df)
        return df
    
    def calculate_variance(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate price variance across sources"""
        variance_data = []
        
        for date in df["Date"].unique():
            date_data = df[df["Date"] == date]
            prices = date_data["Price"].dropna().astype(float)
            
            if len(prices) > 1:
                variance_data.append({
                    "Date": date,
                    "Hotel": date_data["Hotel"].iloc[0],
                    "Min_Price": prices.min(),
                    "Max_Price": prices.max(),
                    "Avg_Price": prices.mean(),
                    "Variance": prices.var(),
                    "Std_Dev": prices.std(),
                    "Price_Range": prices.max() - prices.min(),
                })
        
        return pd.DataFrame(variance_data)
    
    def get_all_hotel_rates(self) -> Dict[str, pd.DataFrame]:
        """Monitor all hotels"""
        all_rates = {}
        
        for hotel_name in HOTELS.keys():
            logger.info(f"Monitoring {hotel_name}...")
            df = self.monitor_daily_rates(hotel_name)
            all_rates[hotel_name] = df
        
        return all_rates
