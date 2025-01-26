# tm-time-tracking

## Overview
This project is designed to track time spent on various tasks and projects. It provides a user-friendly interface for inputting and viewing time entries, making it easier to manage and analyze time usage.

## Features

- Data ingested, cleaned and transformed from a CSV file 
- Filtering and viewing time entries by user 
- Data storage in a database (SQLIte)

## Project Structure

- `constant.py` : Constants and configurations
- `etl.py` : Data ingestion and transformation
- `main.py` : Entry point for the web app
- `requirements.txt` : List of dependencies

## Architecture
![aws_solution-Basic solution drawio](https://github.com/user-attachments/assets/72140c96-2035-413b-a3ec-9f77e4810b0e)

### Data Source
 - the sole data source is a .csv file containing time-tracking information with 4 columns: user, hours, project, and timestamp. 

### Data Extraction (Extract)
 - Ingests the data from the .csv file into a pandas DataFrame.

### Data Transformation (Transform)
 - Cleans the data by removing missing values and converting the 'timestamp' column to datetime format.
 - Rearranges the column names
 - Translates non-English text into English text
 - Convert string datetime to datetime format

### Data Load (Load)
 - Stores the transformed data in a SQLite database.

### Web Service
 - Provides a user-friendly interface for inputting and viewing time entries using Streamlit.


## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd tm-time-tracking

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt

4. **Run the App**
   ```bash
   streamlit run main.py
   ```

5. Access the app locally at [http://localhost:8501](http://localhost:8501)
