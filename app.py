import streamlit as st
import pandas as pd
import sqlite3
from database import create_connection
from update import update_appels 
from importdb import insert_bank

database_path = 'banks_appel_doffre.db'
# Add the form to the Streamlit app
with st.form("add_new_link_form"):
    st.write("Add a New Bank and Link")
    new_bank_name = st.text_input("Bank Name")
    new_bank_url = st.text_input("Bank Link")
    submit_button = st.form_submit_button(label='Add New Link')

    if submit_button:
        if new_bank_name and new_bank_url:
            # Insert the new bank and URL into the database
            conn = create_connection(database_path)
            with conn:
                new_bank_id = insert_bank(conn, (new_bank_name, new_bank_url))
            st.success(f"Added {new_bank_name} with ID {new_bank_id}")
        else:
            st.error("Please provide both the bank name and the link.")


# def fetch_appels_data():
#     """
#     Fetch the latest appel d'offre data from the database.
#     """
#     conn = create_connection(database_path)
#     df = pd.read_sql_query("SELECT b.name, a.keywords_found, a.status, a.first_time_found, a.last_time_checked FROM appels a JOIN banks b ON a.bank_id = b.id", conn)
#     conn.close()
#     return df
def fetch_appels_data():
    """
    Fetch the latest appel d'offre data from the database along with the bank URLs.
    """
    conn = create_connection(database_path)
    query = """
    SELECT b.name, a.keywords_found, a.status, a.first_time_found, a.last_time_checked, b.url 
    FROM appels a 
    JOIN banks b ON a.bank_id = b.id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

st.title('Bank Appel d\'Offre Monitoring System')

if st.button('Update Appel d\'Offre Data'):
    st.text('Updating data...')
    update_appels()
    st.success('Data updated!')

df = fetch_appels_data()
df['Older Offre'] = df.apply(lambda x: '<span style="color:green;">Yes</span>' if x['first_time_found'] == x['last_time_checked'] else '<span style="color:red;">No</span>', axis=1)
#the code here is the first dataframe whch will add the dataframe as a basedatafarme

# if not df.empty:
#     st.write('Current Appel d\'Offre Status:')
#     st.dataframe(df)
# else:
#     st.write('No data available.')
#the code here to add the features of the new column without safe content    
# if not df.empty:
#     st.write('Current Appel d\'Offre Status:')
    
#     # Convert URL column to be clickable and show it in the dataframe
#     df['url'] = df['url'].apply(lambda url: f"[Link]({url})")
    
#     # Display the dataframe
#     st.dataframe(df)
# else:
#     st.write('No data available.')
if not df.empty:
    st.write('Current Appel d\'Offre Status:')
    
    # Convert the URL column to be clickable
    df['url'] = df['url'].apply(lambda url: f"[Link]({url})")

    # Convert the dataframe to HTML and display it
    st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.write('No data available.')
