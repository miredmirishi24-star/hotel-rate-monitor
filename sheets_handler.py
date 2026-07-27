import pandas as pd
from typing import Dict, List
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google.api_python_client import discovery
import logging
from config import GOOGLE_SHEETS_SPREADSHEET_ID, GOOGLE_CREDENTIALS_FILE

logger = logging.getLogger(__name__)

class GoogleSheetsHandler:
    """Handler for Google Sheets integration"""
    
    def __init__(self):
        self.spreadsheet_id = GOOGLE_SHEETS_SPREADSHEET_ID
        self.service = self._authenticate()
        
    def _authenticate(self):
        """Authenticate with Google Sheets API"""
        try:
            credentials = Credentials.from_service_account_file(
                GOOGLE_CREDENTIALS_FILE,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            return discovery.build('sheets', 'v4', credentials=credentials)
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return None
    
    def create_sheet(self, sheet_name: str) -> bool:
        """Create a new sheet"""
        try:
            request = {
                "addSheet": {
                    "properties": {
                        "title": sheet_name
                    }
                }
            }
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body={"requests": [request]}
            ).execute()
            logger.info(f"Sheet '{sheet_name}' created")
            return True
        except Exception as e:
            logger.error(f"Error creating sheet: {str(e)}")
            return False
    
    def write_data(self, sheet_name: str, data: List[List]) -> bool:
        """Write data to sheet"""
        try:
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=f"'{sheet_name}'!A1",
                valueInputOption="RAW",
                body={"values": data}
            ).execute()
            logger.info(f"Data written to '{sheet_name}'")
            return True
        except Exception as e:
            logger.error(f"Error writing data: {str(e)}")
            return False
    
    def highlight_cells(self, sheet_name: str, ranges: List[str], color: Dict) -> bool:
        """Highlight cells with variance"""
        try:
            requests = []
            for cell_range in ranges:
                requests.append({
                    "repeatCell": {
                        "range": self._parse_range(sheet_name, cell_range),
                        "cell": {
                            "userEnteredFormat": {
                                "backgroundColor": color
                            }
                        },
                        "fields": "userEnteredFormat.backgroundColor"
                    }
                })
            
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body={"requests": requests}
            ).execute()
            logger.info(f"Cells highlighted in '{sheet_name}'")
            return True
        except Exception as e:
            logger.error(f"Error highlighting cells: {str(e)}")
            return False
    
    def _parse_range(self, sheet_name: str, cell_range: str) -> Dict:
        """Parse cell range to API format"""
        # Convert A1:B5 format to row/column indices
        parts = cell_range.split(":")
        start = self._cell_to_indices(parts[0])
        end = self._cell_to_indices(parts[1]) if len(parts) > 1 else start
        
        return {
            "sheetId": self._get_sheet_id(sheet_name),
            "startRowIndex": start[0],
            "endRowIndex": end[0] + 1,
            "startColumnIndex": start[1],
            "endColumnIndex": end[1] + 1,
        }
    
    def _cell_to_indices(self, cell: str) -> tuple:
        """Convert cell reference (A1) to row/column indices"""
        col = 0
        for char in cell:
            if char.isalpha():
                col = col * 26 + (ord(char) - ord('A') + 1)
            else:
                row = int(cell[cell.index(char):]) - 1
                return (row, col - 1)
        return (0, col - 1)
    
    def _get_sheet_id(self, sheet_name: str) -> int:
        """Get sheet ID by name"""
        try:
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            for sheet in spreadsheet['sheets']:
                if sheet['properties']['title'] == sheet_name:
                    return sheet['properties']['sheetId']
        except Exception as e:
            logger.error(f"Error getting sheet ID: {str(e)}")
        return 0
