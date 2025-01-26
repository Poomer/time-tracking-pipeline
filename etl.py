import pandas as pd

# Constant module
from constant import Constants

# Language translation frameworks
from langdetect import detect
from deep_translator import GoogleTranslator

# Database
from sqlalchemy import create_engine, text  

# Logging
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


## Ingestion Layer
raw_df = pd.read_csv(Constants.file_name)


# Transfomation Layer
'''
This layer is the processing layer responsible for cleaning the dataset that we explored earlier. So far, we have identified the following flaws:

    - Null values in user column
    - Columns need to be rearraged to make the report looks more readable. For instance, hours column should be located next to timestamp column
    - Various datetime format in timestamp column
    - Some rows in timestamp column contains non-English characters
'''
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


## Stage 1:  Impute null values in user column with a default string value : unknown

# Copy to another df and transform
transformed_df = raw_df.copy(deep=True)

# Then, impute null values in user column
transformed_df.user.fillna('unknown user', inplace=True)

## Stage 2: Rearrange columns
new_ordered_col = ['user', 'project', 'hours', 'timestamp']
transformed_df = transformed_df[new_ordered_col]
transformed_df_list = [transformed_df.iloc[i:i + Constants.chunk_size] for i in range(0, len(transformed_df), Constants.chunk_size)]

## Stage 3: Translate non-English text in timestamp column into English text
count_stage3 = 0

for df in transformed_df_list:

    try:
          
        df['trans_timestamp'] = df['timestamp'].apply(detect_and_translate)


    except Exception:
        
        logger.error(f"Failed to translate at batch {count_stage3} due to {Exception}")
        raise(Exception)

    count_stage3 = count_stage3+1

## Stage 4: Convert values in trans_timestamp column into those of datetime type in the new column: datetime_col

count_stage4 = 0

for df in transformed_df_list:

    try:      
        df['datetime_col'] = pd.to_datetime(df['trans_timestamp'], format="mixed")

    except Exception:
        
        logger.error(f"Failed to convert to datetime column at batch {count_stage4} due to {Exception}")
        raise(Exception)

    count_stage4 += 1

## Stage 5-6: Final Cleaning

## Drop origninal timestamp columns
count_stage5 = 0

for df in transformed_df_list:

    try:
        df.drop(columns=['timestamp', 'trans_timestamp'], inplace=True)

    except Exception:
        logger.error(f"Failed to drop columns at batch {count_stage5} due to {Exception}")
        raise(Exception)

    count_stage5 += 1

## Rename the latest timestamp column as timestamp column
count_stage6 = 0

for df in transformed_df_list:

    try:
        df.rename(columns={"datetime_col" : "timestamp"}, inplace=True, errors="raise")

    except Exception:
        logger.error(f"Failed to rename column at batch {count_stage6} due to {Exception}")
        raise(Exception)

    count_stage6 += 1


## Load Layer

url = f'sqlite:///' + Constants.database
sqlite_engine = create_engine(url)

logger.info("Connecting to the database...")

# Load data from the list of dataframes into the database
for df in transformed_df_list:
    df.to_sql(Constants.table_name, sqlite_engine, if_exists='append', index=False)
