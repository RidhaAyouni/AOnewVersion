import sqlite3
from database import create_connection, insert_appel, update_appel
from scraper import scrape_bank
from datetime import datetime

database_path = 'banks_appel_doffre.db'

def fetch_banks_data():
    """
    Fetch all bank records from the database.
    """
    conn = create_connection(database_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM banks")
    banks = cur.fetchall()
    conn.close()
    return banks

def update_bank_appel(bank_id, keywords_found, status, first_time_found, last_time_checked):
    """
    Update the appel d'offre details for a bank.
    """
    conn = create_connection(database_path)
    with conn:
        # Check if there's an existing record
        cur = conn.cursor()
        cur.execute("SELECT * FROM appels WHERE bank_id=?", (bank_id,))
        existing = cur.fetchone()
        
        if existing:
            # Update existing record
            update_appel(conn, bank_id, keywords_found, status, last_time_checked)
        else:
            # Insert new record
            insert_appel(conn, bank_id, keywords_found, status, first_time_found, last_time_checked)

def update_appels():
    """
    The main function to fetch the latest "appel d'offre" data and update the database.
    """
    banks = fetch_banks_data()
    for bank in banks:
        bank_id, name, url = bank
        keywords_found = scrape_bank(url)
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if keywords_found:
            # Determine the status based on keywords found
            status = 'New AO'  # Logic to determine if it's 'New AO' or 'Classic AO'
            first_time_found = now  # Or fetch from the database if it's an update
            update_bank_appel(bank_id, ','.join(keywords_found), status, first_time_found, now)
        else:
            update_bank_appel(bank_id, '', 'No AO', '', now)

if __name__ == "__main__":
    update_appels()
