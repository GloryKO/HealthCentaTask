
from utils import *
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
def main(file_path: str, api_url: str) -> None:
    """
    Main function to run the data processing pipeline.

    Args:
        file_path (str): Path to the Excel file.
        api_url (str): URL of the API server.
    """
    try:
        logger.info("Starting data processing pipeline")
        
        df = read_excel_file(file_path)
        logger.info("Excel file read successfully")
        
        cleaned_df = clean_data(df)
        logger.info("Data cleaned successfully")
        
        transformed_data = transform_data(cleaned_df)
        logger.info("Data transformed successfully")
        
        json_data = generate_json(transformed_data)
        logger.info("JSON data generated successfully")

        logger.info("Sending data to API server...")
        response = send_to_server(json_data, api_url)
        
        logger.info(f"API Response Status Code: {response.status_code}")
        logger.info(f"API Response Content: {response.text}")
        
        logger.info("Data processing pipeline completed successfully,Check server logs for data")
    except Exception as e:
        logger.exception(f"An error occurred during the data processing pipeline: {e}")

if __name__ == "__main__":
    file_path = "/home/glory-ko/HealthCentaTask/Sample data.xls"
    api_url = "http://localhost:8000"  # URL for the mock API server
    main(file_path, api_url)

