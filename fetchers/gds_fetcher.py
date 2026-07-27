import requests
from typing import Dict, Optional
from .base_fetcher import BaseFetcher
import logging
from config import GDS_API_KEY

logger = logging.getLogger(__name__)

class GDSFetcher(BaseFetcher):
    """Fetcher for GDS (Global Distribution System) hotel rates"""
    
    def __init__(self):
        super().__init__("GDS")
        self.api_key = GDS_API_KEY
        self.base_url = "https://api.gds-global.com/v1"
        
    def fetch_rate(self, hotel_name: str, check_in: str, check_out: str) -> Optional[Dict]:
        """Fetch rate from GDS API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            
            params = {
                "hotelName": hotel_name,
                "checkInDate": check_in,
                "checkOutDate": check_out,
            }
            
            response = requests.get(
                f"{self.base_url}/hotels/availability",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("rooms"):
                    room = data["rooms"][0]
                    rate_data = self.parse_rate_response({
                        "price": room.get("rate", {}).get("amount"),
                        "currency": room.get("rate", {}).get("currency"),
                        "available": room.get("available"),
                        "room_type": room.get("roomType"),
                        "nights": room.get("numberOfNights"),
                    })
                    return rate_data if self.validate_rate_data(rate_data) else None
        except Exception as e:
            logger.error(f"GDS fetch error for {hotel_name}: {str(e)}")
        
        return None
