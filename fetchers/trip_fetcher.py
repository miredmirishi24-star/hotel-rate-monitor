import requests
from typing import Dict, Optional
from .base_fetcher import BaseFetcher
import logging
from config import TRIP_API_KEY

logger = logging.getLogger(__name__)

class TripFetcher(BaseFetcher):
    """Fetcher for Trip.com hotel rates"""
    
    def __init__(self):
        super().__init__("Trip.com")
        self.api_key = TRIP_API_KEY
        self.base_url = "https://api.trip.com/v1"
        
    def fetch_rate(self, hotel_name: str, check_in: str, check_out: str) -> Optional[Dict]:
        """Fetch rate from Trip.com API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            
            params = {
                "keyword": hotel_name,
                "checkin": check_in,
                "checkout": check_out,
            }
            
            response = requests.get(
                f"{self.base_url}/hotel/search",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("hotelList"):
                    hotel = data["hotelList"][0]
                    rate_data = self.parse_rate_response({
                        "price": hotel.get("lowestPrice"),
                        "currency": hotel.get("currency"),
                        "available": hotel.get("available", True),
                        "room_type": hotel.get("roomType"),
                        "nights": hotel.get("numberOfNights"),
                    })
                    return rate_data if self.validate_rate_data(rate_data) else None
        except Exception as e:
            logger.error(f"Trip.com fetch error for {hotel_name}: {str(e)}")
        
        return None
