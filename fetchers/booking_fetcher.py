import requests
from typing import Dict, Optional
from .base_fetcher import BaseFetcher
import logging
from config import BOOKING_API_KEY

logger = logging.getLogger(__name__)

class BookingFetcher(BaseFetcher):
    """Fetcher for Booking.com hotel rates"""
    
    def __init__(self):
        super().__init__("Booking.com")
        self.api_key = BOOKING_API_KEY
        self.base_url = "https://api.booking.com/v1"
        
    def fetch_rate(self, hotel_name: str, check_in: str, check_out: str) -> Optional[Dict]:
        """Fetch rate from Booking.com API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            
            params = {
                "name": hotel_name,
                "checkin_date": check_in,
                "checkout_date": check_out,
            }
            
            response = requests.get(
                f"{self.base_url}/accommodations",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("accommodations"):
                    accommodation = data["accommodations"][0]
                    rate_data = self.parse_rate_response({
                        "price": accommodation.get("price_breakdown", {}).get("total_price"),
                        "currency": accommodation.get("currency_code"),
                        "available": accommodation.get("available"),
                        "room_type": accommodation.get("room_type"),
                        "nights": accommodation.get("number_of_nights"),
                    })
                    return rate_data if self.validate_rate_data(rate_data) else None
        except Exception as e:
            logger.error(f"Booking fetch error for {hotel_name}: {str(e)}")
        
        return None
