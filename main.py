import streamlit as st
import pandas as pd 
from sqlalchemy import create_engine, text

import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


DATABASE_URL = "sqlite:///data_checkins.db"
engine = create_engine(DATABASE_URL)

# Fetch unique users
def get_unique_users() -> tuple[str]:
    """
    Fetch a list of unique users.

    Returns
    -------
    tuple[str]
        A tuple of unique users.

    """
    with engine.connect() as conn:
        logger.info("Fetch a list of unique users")
        exe = conn.execute(text('SELECT DISTINCT(user) FROM data_check_ins'))
        result = exe.fetchall()
        result_tuple = tuple(name for (name,) in result)
    
    return result_tuple

# Fetch check-ins for a specific user
def get_checkins(user):
    """
    Fetch all check-ins for a specific user.

    Parameters
    ----------
    user: str
        The user to fetch check-ins for.

    Returns
    -------
    df: pandas.DataFrame
        A DataFrame containing the check-ins for the specified user.
    """

    with engine.connect() as conn:
        logger.info("Get check-ins for a specific user")
        query = text(f"SELECT * FROM data_check_ins WHERE user = '{user}'")
        result = conn.execute(query)
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df

##----- Entry point of the web app -----

# Streamlit app layout
st.title("User Check-ins")

# Get unique users for the dropdown
users = get_unique_users()  ## This must return a list of users as a tuple

selected_user = st.selectbox("Select a user:", users)


# Return all rows for a selected user
if selected_user:

    checkins = get_checkins(selected_user) 

    st.write(f"The following is a list of check-ins for {selected_user}")

    st.dataframe(checkins, width=1000, height=500)

    '''
    # Safe version
    if not checkins.empty:
        st.write(f"The following is a list of check-ins for {selected_user}", checkins)
    else:
        st.write("No check-ins found for this user.")
    '''
    




