from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class BaseFetcher(ABC):
    """Base class for hotel rate fetchers"""
    
    def __init__(self, source_name: str):
        self.source_name = source_name
        self.rates = {}
        
    @abstractmethod
    def fetch_rate(self, hotel_name: str, check_in: str, check_out: str) -> Optional[Dict]:
        """Fetch rate for a hotel
        
        Args:
            hotel_name: Name of the hotel
            check_in: Check-in date (YYYY-MM-DD)
            check_out: Check-out date (YYYY-MM-DD)
            
        Returns:
            Dict with rate data or None if fetch failed
        """
        pass
    
    def parse_rate_response(self, response: Dict) -> Dict:
        """Parse rate response to standard format"""
        return {
            "source": self.source_name,
            "price": response.get("price"),
            "currency": response.get("currency", "USD"),
            "availability": response.get("available", True),
            "timestamp": datetime.now().isoformat(),
            "room_type": response.get("room_type"),
            "nights": response.get("nights"),
        }
    
    def validate_rate_data(self, rate_data: Dict) -> bool:
        """Validate rate data integrity"""
        required_fields = ["price", "currency", "timestamp"]
        return all(field in rate_data for field in required_fields)
