import pandas as pd
import json
from typing import List, Dict, Any
import requests
import logging
from requests.exceptions import RequestException

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def read_excel_file(file_path: str) -> pd.DataFrame:
    """
    Read the Excel file and return a pandas DataFrame.

    Args:
        file_path (str): Path to the Excel file.

    Returns:
        pd.DataFrame: The data from the Excel file.

    Raises:
        FileNotFoundError: If the file is not found.
        pd.errors.EmptyDataError: If the file is empty.
        Exception: For any other errors during file reading.
    """
    try:
        df = pd.read_excel(file_path, header=0)
        logger.info(f"Successfully read Excel file. Shape: {df.shape}")
        logger.debug(f"Columns: {df.columns.tolist()}")
        return df
    except FileNotFoundError:
        logger.error(f"Excel file not found: {file_path}")
        raise
    except pd.errors.EmptyDataError:
        logger.error(f"Excel file is empty: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Error reading Excel file: {str(e)}")
        raise

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the data by handling missing values and removing duplicates.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    logger.info(f"Shape before cleaning: {df.shape}")
    logger.debug(f"Null values in columns: {df.isnull().sum().to_dict()}")

    # Drop rows with all NaN values
    df = df.dropna(how='all')
    
    # Strip whitespace from column names
    df.columns = df.columns.str.strip()

    # Drop the empty column (assuming it's always the 7th column)
    df= df.drop(df.columns[6],axis=1)
    # Drop rows where 'SERVICE' contains 'HEART' or 'HEAD' as they are not needed in the JSON structure
   
    df = df[(df['SERVICE'] != 'HEART') & (df['SERVICE'] != 'HEAD')].copy()

    # Drop remaining rows with any NaN values
    df = df.dropna()

    # Remove duplicate rows
    df = df.drop_duplicates()
    logger.info(f"Shape after cleaning: {df.shape}")
    return df

def transform_data(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Transform the data into the desired format for the API.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        List[Dict[str, Any]]: The transformed data.
    """
    transformed_data = []
    
    for _, row in df.iterrows():
        try:
            service_data = {
                "name": row['SERVICE'],
                "product_index": row['PRODUCT INDEX'],
                "department": {'name': row['DEPARTMENT']},
                "speciality": {'name': row['SPECIALTY']},
                "category": {'name': row['CATEGORY']},
                "nature_of_procedure": {'name': row['NATURE OF ENT. PROCEDURE']},
                "service_providers": [
                    {"id": i, "price": row[f'SP. {i}']} for i in range(1, 5)
                ]
            }
            transformed_data.append(service_data)
        except KeyError as e:
            logger.error(f"Missing key in row: {e}")
        except ValueError as e:
            logger.error(f"Value error in row: {e}")
    
    logger.info(f"Transformed {len(transformed_data)} rows")
    return transformed_data

def generate_json(data: List[Dict[str, Any]]) -> str:
    """
    Generate JSON from the transformed data.

    Args:
        data (List[Dict[str, Any]]): The data to be converted to JSON.

    Returns:
        str: The JSON string representation of the data.
    """
    return json.dumps(data, indent=2)

def send_to_server(json_data: str, api_url: str) -> requests.Response:
    """
    Send the JSON data to the specified API endpoint.

    Args:
        json_data (str): The JSON data to send.
        api_url (str): The URL of the API endpoint.

    Returns:
        requests.Response: The response from the server.

    Raises:
        RequestException: If there's an error sending the request.
    """
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(api_url, data=json_data, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response
    except RequestException as e:
        logger.error(f"Error sending data to server: {e}")
        raise