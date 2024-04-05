import streamlit as st
import pandas as pd
import sqlite3
from database import create_connection
from update import update_appels 

database_path = 'banks_appel_doffre.db'

def fetch_appels_data():
    """
    Fetch the latest appel d'offre data from the database.
    """
    conn = create_connection(database_path)
    df = pd.read_sql_query("SELECT b.name, a.keywords_found, a.status, a.first_time_found, a.last_time_checked FROM appels a JOIN banks b ON a.bank_id = b.id", conn)
    conn.close()
    return df

st.title('Bank Appel d\'Offre Monitoring System')

if st.button('Update Appel d\'Offre Data'):
    st.text('Updating data...')
    update_appels()
    st.success('Data updated!')

df = fetch_appels_data()

if not df.empty:
    st.write('Current Appel d\'Offre Status:')
    st.dataframe(df)
else:
    st.write('No data available.')
