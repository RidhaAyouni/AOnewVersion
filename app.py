
import streamlit as st
import pandas as pd
import sqlite3
from database import create_connection
from update import update_appels
from importdb import insert_bank, delete_bank

database_path = 'banks_appel_doffre.db'


st.title("Manage Keywords")

# --- View existing keywords ---
conn = create_connection(database_path)
df_keywords = pd.read_sql_query("SELECT id, keyword FROM keywords ORDER BY keyword ASC", conn)
conn.close()

st.subheader("Existing Keywords")
if not df_keywords.empty:
    st.dataframe(df_keywords, use_container_width=True)
else:
    st.write("No keywords found.")

# --- Add new keyword ---
with st.form("add_keyword_form"):
    new_keyword = st.text_input("Enter a new keyword")
    add_keyword_button = st.form_submit_button(label="Add Keyword")

    if add_keyword_button:
        if new_keyword.strip():
            conn = create_connection(database_path)
            try:
                with conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT OR IGNORE INTO keywords (keyword) VALUES (?)", (new_keyword.strip(),))
                    conn.commit()
                st.success(f"Keyword '{new_keyword}' added successfully.")
            except Exception as e:
                st.error(f"Error adding keyword: {e}")
            finally:
                conn.close()
        else:
            st.error("Please enter a valid keyword.")

# --- Delete selected keyword ---
with st.form("delete_keyword_form"):
    st.subheader("Delete a Keyword")
    conn = create_connection(database_path)
    df_keywords = pd.read_sql_query("SELECT id, keyword FROM keywords ORDER BY keyword ASC", conn)
    conn.close()

    if not df_keywords.empty:
        keyword_options = df_keywords.set_index('id')['keyword'].to_dict()
        selected_keyword_id = st.selectbox("Select a keyword to delete", list(keyword_options.keys()),
                                           format_func=lambda x: keyword_options[x])
        delete_keyword_button = st.form_submit_button(label="Delete Keyword")

        if delete_keyword_button:
            conn = create_connection(database_path)
            try:
                with conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM keywords WHERE id = ?", (selected_keyword_id,))
                    conn.commit()
                st.success(f"Keyword '{keyword_options[selected_keyword_id]}' deleted successfully.")
            except Exception as e:
                st.error(f"Error deleting keyword: {e}")
            finally:
                conn.close()
    else:
        st.write("No keywords available to delete.")

st.title('Add new Link')
with st.form("add_new_link_form"):
    st.write("Add a New Bank and Link")
    new_bank_name = st.text_input("Bank Name")
    new_bank_url = st.text_input("Bank Link")
    submit_button = st.form_submit_button(label='Add New Link')

    if submit_button:
        if new_bank_name and new_bank_url:
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
    st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.write('No data available.')

st.title('Delete Link')
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

