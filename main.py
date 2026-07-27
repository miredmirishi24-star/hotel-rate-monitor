import logging
from datetime import datetime
import pandas as pd
from rate_monitor import RateMonitor
from sheets_handler import GoogleSheetsHandler
from config import HOTELS, OUTPUT_DIR
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def ensure_output_directory():
    """Ensure output directory exists"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def export_to_excel(data: dict, filename: str) -> bool:
    """Export data to Excel with formatting"""
    try:
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            for hotel_name, df in data.items():
                sheet_name = hotel_name[:31]  # Excel sheet name limit
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        logger.info(f"Data exported to {filename}")
        return True
    except Exception as e:
        logger.error(f"Error exporting to Excel: {str(e)}")
        return False

def main():
    logger.info("Starting Hotel Rate Monitor")
    ensure_output_directory()
    
    # Initialize monitor
    monitor = RateMonitor()
    
    # Fetch rates for all hotels
    logger.info("Fetching rates for all hotels...")
    all_rates = monitor.get_all_hotel_rates()
    
    # Calculate variance for each hotel
    variance_data = {}
    for hotel_name, df in all_rates.items():
        variance_data[hotel_name] = monitor.calculate_variance(df)
    
    # Export to local Excel
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_file = os.path.join(OUTPUT_DIR, f"hotel_rates_{timestamp}.xlsx")
    export_to_excel(all_rates, excel_file)
    
    # Upload to Google Sheets if configured
    if any([HOTELS]):
        try:
            sheets = GoogleSheetsHandler()
            for hotel_name, df in all_rates.items():
                sheet_name = f"{hotel_name} Rates"
                sheets.create_sheet(sheet_name)
                
                # Prepare data for sheets
                data = [df.columns.tolist()] + df.values.tolist()
                sheets.write_data(sheet_name, data)
                
                logger.info(f"Uploaded data for {hotel_name} to Google Sheets")
        except Exception as e:
            logger.warning(f"Google Sheets upload failed: {str(e)}")
    
    logger.info("Hotel Rate Monitor completed successfully")
    
    # Display summary
    print("\n" + "="*60)
    print("HOTEL RATE MONITORING SUMMARY")
    print("="*60)
    for hotel_name, df in all_rates.items():
        print(f"\n{hotel_name}:")
        print(f"  Total records: {len(df)}")
        print(f"  Date range: {df['Date'].min()} to {df['Date'].max()}")
        print(f"  Sources: {', '.join(df['Source'].unique())}")
        if hotel_name in variance_data:
            var_df = variance_data[hotel_name]
            print(f"  Avg price: ${var_df['Avg_Price'].mean():.2f}")
            print(f"  Max variance: ${var_df['Price_Range'].max():.2f}")

if __name__ == "__main__":
    main()
