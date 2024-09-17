# HealthCenta Data Processing

This project processes healthcare-related data from an Excel file, transforms it into a specific JSON format, and prepares it for API submission.

## *Setup*

1. Ensure you have *Python 3.7+* installed on your system.

2. Clone this repository:
   bash
   git clone https://github.com/GloryKO/HealthCentaTask.git
   

3. Navigate into the project directory:
   bash
   cd HealthCentaTask
   

4. Create a virtual environment and activate it:

   - *On Linux/macOS*:
     bash
     python -m venv env
     source env/bin/activate
     

   - *On Windows*:
     bash
     python -m venv env
     env\Scripts\activate
     

5. Install the required packages:
   bash
   pip install -r requirements.txt
   

---

## *Usage*

1. Place your Excel file in the project directory.

2. Update the file_path variable in main.py to point to your Excel file.

3. Run the scripts:
   - First, start the mock server:
     bash
     python mock_server.py
     
   - Then, run the main processing script:
     bash
     python main.py
     

4. The processed JSON data will be printed to the console.  
   - To send the data to an API, *uncomment* the relevant lines in the main() function and update the api_url variable with the correct endpoint.

---

## *How It Works*

- *read_excel_file()*: Reads the Excel file using pandas.
  
- *clean_data()*: Removes any rows with missing values or duplicates.

- *transform_data()*: Converts the DataFrame into the required JSON structure.

- *generate_json()*: Converts the transformed data into a JSON string.

- *send_to_server()*: Sends the JSON data to a mock server.

The main() function orchestrates these steps by calling the other functions from utils.py.

---

## *Notes*

- The script includes *error handling* for file reading and data processing.
- Print statements are used to display some data in the terminal (this may not be ideal for a production environment).
- A *mock server* has been set up to simulate how this data might be submitted to an endpoint.