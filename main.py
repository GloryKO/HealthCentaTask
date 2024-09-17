
from utils import *

def main(file_path: str, api_url: str) -> None:
    """
    Main function to run the data processing pipeline.
    """
    df = read_excel_file(file_path)
    cleaned_df = clean_data(df)
    transformed_data = transform_data(cleaned_df)
    json_data = generate_json(transformed_data)

    
    print("\nSending data to mock API server...")
    response = send_to_server(json_data, api_url)
    print(f"API Response Status Code: {response.status_code}")
    print(f"API Response Content: {response.text}")

if __name__ == "__main__":
    file_path = "/home/glory-ko/HealthCentaTask/Sample data.xls"
    api_url = "http://localhost:8000"  # URL for the mock API server
    main(file_path, api_url)