import pandas as pd
import json
from typing import List, Dict, Any
import requests
import sys

def read_excel_file(file_path: str) -> pd.DataFrame:
    """
    Read the Excel file and return a pandas DataFrame.
    """
    try:
        df = pd.read_excel(file_path, header=0) 
        print(f"Successfully read Excel file. Shape: {df.shape}")
        # print(f"Columns: {df.columns.tolist()}")
        return df
    except Exception as e:
        print(f"Error reading Excel file: {str(e)}")
        sys.exit(1)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the data by handling missing values and removing duplicates.
    """
    print(f"Shape before cleaning: {df.shape}")
    print("-------------------------------------------------------------------------------------------------------------")
    print(f"sum of all null values in columns: {df.isnull().sum()}")

    #drop row with all Nan value
    df=df.dropna(how='all') 
    df.columns = df.columns.str.strip()

    #drop the empty column
    df.drop(df.columns[6],axis=1,inplace=True)
    #drop rows where 'SERVICE' contains 'HEART' or 'HEAD'(as it is not required in the expected JSON response)
    df = df[(df['SERVICE'] != 'HEART') & (df['SERVICE'] != 'HEAD')]
    #df=df.fillna('null') #replace remaining Nan values with null
    df=df.dropna()
    print(df)
    df = df.drop_duplicates() #remove any duplicate data
    print("--------------------------------------------------------------------------------------------------------------") 
    print(f"Shape after cleaning: {df.shape}")
    return df

def transform_data(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Transform the data into the desired format for the API.
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
                    {"id": 1, "price": (row['SP. 1'])},
                    {"id": 2, "price": (row['SP. 2'])},
                    {"id": 3, "price": (row['SP. 3'])},
                    {"id": 4, "price": (row['SP. 4'])}
                ]
            }
            transformed_data.append(service_data)
        except KeyError as e:
            print(f"Error transforming row: {row}")
            print(f"Missing key: {str(e)}")
        except ValueError as e:
            print(f"Error transforming row: {row}")
            print(f"Value error: {str(e)}")
    
    print(f"Transformed {len(transformed_data)} rows")
    return transformed_data

def generate_json(data: List[Dict[str, Any]]) -> str:
    """
    Generate JSON from the transformed data.
    """
    return json.dumps(data, indent=2)

def send_to_server(json_data: str, api_url: str) -> requests.Response:
    """
    Send the JSON data to the specified API endpoint.
    """
    headers = {'Content-Type': 'application/json'}
    response = requests.post(api_url, data=json_data, headers=headers)
    return response
