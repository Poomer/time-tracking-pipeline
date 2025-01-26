import pandas as pd
import numpy as np
import datetime

from constant import chunk_size, file_name, database

from langdetect import detect
from deep_translator import GoogleTranslator

from sqlalchemy import create_engine, text  

import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)



## Ingestion Layer
raw_df = pd.read_csv('dailycheckins.csv')

## Split a single large dataframe into small ones
raw_df_list = [raw_df.iloc[i:i + chunk_size] for i in range(0, len(raw_df), chunk_size)]


# Transfomation Layer

## Stage 1:

# Copy to another df and transform
transformed_df_list = raw_df_list

count = 0

for df in transformed_df_list:
    
    # Translate a non-english text and add a new column called trans_timestamp
    df['trans_timestamp'] = df['timestamp'].apply(detect_and_translate)

## Stage 2: Create a datetime column from trans_timestamp
count_stage2 = 0

for df in transformed_df_list:

    try:      
        df['datetime_col'] = pd.to_datetime(df['trans_timestamp'], format="mixed")

    except Exception:
        
        logger.error(f"Failed to convert to datetime column at batch {count_stage2} due to {Exception}")
        raise(Exception)

    count_stage2 += 1

## Stage 3:

count_stage3 = 0

for df in transformed_df_list:

    print(f"dataframe : {count}")

    # Drop columns
    try:    
        df.drop(columns=['timestamp', 'trans_timestamp'], inplace=True)
    except Exception:

        logger.error(f"Failed to drop columns at batch {count_stage3} due to {Exception}")
        raise(Exception)

    count_stage3 += 1

## Stage 4: Rename datetime_col as timestamp

for df in transformed_df_list:

    print(f"dataframe : {count}")

    # Rename datetime_col as timestamp
    df.rename(columns={"datetime_col" : "timestamp"}, inplace=True, errors="raise")
  
    count = count+1


# Validation Layer






## Load Layer

url = f'sqlite:///' + database
sqlite_engine = create_engine(url)

# Load data from the list of dataframes into the database
for df in transformed_df_list:
    df.to_sql(name='data_check', con=sqlite_engine, if_exists='append', index=False)


## Auxliary functions
def detect_and_translate(text:str) -> str:
    """
    Detect language and translate if needed.

    Parameters
    ----------
    text : str
        The text to translate.

    Returns
    -------
    str
        The translated text.
    """

    if pd.isna(text):
        return text

    try:
        # Detect language
        lang = detect(str(text))
        #print(lang)

        if lang in ['ru', 'uk', 'bg']:
            translator = GoogleTranslator(source='auto', target='en')
            return translator.translate(text)
        return text
            
    except Exception as e:

        logger.error(f"Failed to detect and translate text due to {e}")
        raise(e)