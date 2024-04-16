# import streamlit as st
# import pandas as pd
# import sqlite3
# from database import create_connection
# from update import update_appels 
# from importdb import insert_bank , delete_bank

# database_path = 'banks_appel_doffre.db'
# st.title('Add new Bank ')
# # Add the form to the Streamlit app
# with st.form("add_new_link_form"):
#     st.write("Add a New Bank and Link")
#     new_bank_name = st.text_input("Bank Name")
#     new_bank_url = st.text_input("Bank Link")
#     submit_button = st.form_submit_button(label='Add New Link')

#     if submit_button:
#         if new_bank_name and new_bank_url:
#             # Insert the new bank and URL into the database
#             conn = create_connection(database_path)
#             with conn:
#                 new_bank_id = insert_bank(conn, (new_bank_name, new_bank_url))
#             st.success(f"Added {new_bank_name} with ID {new_bank_id}")
#         else:
#             st.error("Please provide both the bank name and the link.")


# def fetch_appels_data():
#     conn = create_connection(database_path)
#     query = """
#     SELECT b.name, a.keywords_found, a.status, a.first_time_found, a.last_time_checked, b.url 
#     FROM appels a 
#     JOIN banks b ON a.bank_id = b.id
#     """
#     df = pd.read_sql_query(query, conn)
#     conn.close()
#     return df

# st.title('Bank Appel d\'Offre Monitoring System')

# if st.button('Update Appel d\'Offre Data'):
#     update_appels()
#     st.success('Data updated!')

# df = fetch_appels_data()
# if not df.empty:
#     df['Older Offre'] = df.apply(lambda x: '<span style="color:green;">Yes</span>' if x['first_time_found'] == x['last_time_checked'] else '<span style="color:red;">No</span>', axis=1)
#     # Convert the URL column to a clickable link styled as a button
#     df['Action'] = df['url'].apply(lambda url: f'<a href="{url}" target="_blank" style="display:inline-block; background-color:#0078D4; color:white; padding:8px 12px; text-align:center; border-radius:5px; text-decoration:none;">Go to Link</a>')

#     df.rename(columns={
#         'Bank_Name': 'Bank Name',
#         'Keywords_Found': 'Keywords Detected',
#         'Status': 'Current Status',
#         'First_Detection_Date': 'First Detected',
#         'Last_Checked_Date': 'Last Checked',
#         'Is_Older_Tender': 'Tender Unchanged',
#         'Action': 'Visit Bank Page'
#     }, inplace=True)
#     # Convert the dataframe to HTML and display it using unsafe_allow_html to render HTML
#     st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)
# else:
#     st.write('No data available.')
# st.title('Delete Bank ')
# with st.form("delete_bank_form"):
#     st.write("Delete a Bank")
#     conn = create_connection(database_path)
#     df_banks = pd.read_sql_query("SELECT id, name FROM banks", conn)
#     conn.close()
#     bank_options = df_banks.set_index('id')['name'].to_dict()
#     selected_bank_id = st.selectbox("Select Bank to Delete", list(bank_options.keys()), format_func=lambda x: bank_options[x])
#     delete_button = st.form_submit_button(label='Delete Selected Bank')

#     if delete_button:
#         conn = create_connection(database_path)
#         with conn:
#             delete_bank(conn, selected_bank_id)
#         st.success(f"Deleted Bank ID: {selected_bank_id}")
import streamlit as st
import pandas as pd
import sqlite3
from database import create_connection
from update import update_appels
from importdb import insert_bank, delete_bank

database_path = 'banks_appel_doffre.db'
st.title('Add new Bank')
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

def fetch_appels_data():
    conn = create_connection(database_path)
    query = """
    SELECT b.name AS 'Bank Name', a.keywords_found AS 'Keywords Detected', a.status AS 'Current Status', 
           a.first_time_found AS 'First Detected', a.last_time_checked AS 'Last Checked', b.url AS 'URL'
    FROM appels a 
    JOIN banks b ON a.bank_id = b.id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    df['Older Offre'] = df.apply(lambda x: 'Yes' if x['First Detected'] == x['Last Checked'] else 'No', axis=1)
    df['Action'] = df['URL'].apply(lambda url: f'<a href="{url}" target="_blank" style="display:inline-block; background-color:#0078D4; color:white; padding:8px 12px; text-align:center; border-radius:5px; text-decoration:none;">Go to Link</a>')
    return df.sort_values(by='Older Offre', ascending=False)

st.title('Bank Appel d\'Offre Monitoring System')

if st.button('Update Appel d\'Offre Data'):
    update_appels()
    st.success('Data updated!')

df = fetch_appels_data()
if not df.empty:
    # Convert the dataframe to HTML and display it using unsafe_allow_html to render HTML
    st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.write('No data available.')

st.title('Delete Bank')
with st.form("delete_bank_form"):
    st.write("Delete a Bank")
    conn = create_connection(database_path)
    df_banks = pd.read_sql_query("SELECT id, name FROM banks", conn)
    conn.close()
    bank_options = df_banks.set_index('id')['name'].to_dict()
    selected_bank_id = st.selectbox("Select Bank to Delete", list(bank_options.keys()), format_func=lambda x: bank_options[x])
    delete_button = st.form_submit_button(label='Delete Selected Bank')

    if delete_button:
        conn = create_connection(database_path)
        with conn:
            delete_bank(conn, selected_bank_id)
        st.success(f"Deleted Bank ID: {selected_bank_id}")

