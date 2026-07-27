import requests
from typing import Dict, Optional
from .base_fetcher import BaseFetcher
import logging
from config import EXPEDIA_API_KEY

logger = logging.getLogger(__name__)

class ExpediaFetcher(BaseFetcher):
    """Fetcher for Expedia hotel rates"""
    
    def __init__(self):
        super().__init__("Expedia")
        self.api_key = EXPEDIA_API_KEY
        self.base_url = "https://open.expediagroup.com/v2"
        
    def fetch_rate(self, hotel_name: str, check_in: str, check_out: str) -> Optional[Dict]:
        """Fetch rate from Expedia API"""
        try:
            # This is a placeholder - actual implementation would use Expedia's Rapid API
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            
            params = {
                "query": hotel_name,
                "checkin": check_in,
                "checkout": check_out,
                "currency": "USD",
            }
            
            # Mock endpoint - replace with actual Expedia endpoint
            response = requests.get(
                f"{self.base_url}/search",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                rate_data = self.parse_rate_response({
                    "price": data.get("properties", [{}])[0].get("lowest_price"),
                    "currency": "USD",
                    "available": data.get("properties", [{}])[0].get("available"),
                    "room_type": "Standard",
                    "nights": (datetime.strptime(check_out, "%Y-%m-%d") - datetime.strptime(check_in, "%Y-%m-%d")).days,
                })
                return rate_data if self.validate_rate_data(rate_data) else None
        except Exception as e:
            logger.error(f"Expedia fetch error for {hotel_name}: {str(e)}")
        
        return None
