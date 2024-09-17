# HealthCenta Data Processing
This project processes healthcare-related data from an Excel file, transforms it into a specific JSON format, and prepares it for API submission.

* Setup

Ensure you have Python 3.7+ installed on your system.
Clone this repository:
 `https://github.com/GloryKO/HealthCentaTask.git`

 cd into the project file:
 `cd HealthCentaTask`

Create a virtual environment and activate it:

 `python -m venv env`
 `source env/bin/activate  (On Windows, use `env\Scripts\activate`)`

* Install the required packages:
    `pip install -r requirements.txt`


* Usage

    Place your Excel file in the project directory.
    Update the file_path variable in main.py to point to your Excel file.

    Run the scripts:
    `python mock_server.py ` ( makes sure the server runs first)
    `python main.py`  (this then run the main file)

    The processed JSON data will be printed to the console.
    To send the data to an API, uncomment the relevant lines in the main() function and update the api_url variable with the correct endpoint.


* How It Works

    read_excel_file(): Reads the Excel file using pandas.
    clean_data(): Removes any rows with missing values , duplicates.
    transform_data(): Converts the DataFrame into the required JSON structure.
    generate_json(): Converts the transformed data into a JSON string.
    send_to_server(): Sends the JSON data to a mock server.

    The main() function orchestrates these steps by calling the other functions from utils.

# Notes

The script includes error handling for file reading and data processing.
I have used print statements to display some data in the terminal (may not be best for production enviroment)
I have setup a mock server just to be able to mock how this data may be submitted to an endpoint