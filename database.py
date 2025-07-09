import sqlite3
from sqlite3 import Error

database_path = 'banks_appel_doffre.db'

def create_connection(db_file):
    """Create a database connection to a SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """Create a table from the create_table_sql statement"""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

sql_create_banks_table = """
CREATE TABLE IF NOT EXISTS banks (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT NOT NULL
);
"""
sql_create_domain_keywords_table = """
CREATE TABLE IF NOT EXISTS keywords (
    id INTEGER PRIMARY KEY,
    keyword TEXT NOT NULL,
);
"""

sql_create_appels_table = """
CREATE TABLE IF NOT EXISTS appels (
    id INTEGER PRIMARY KEY,
    bank_id INTEGER NOT NULL,
    keywords_found TEXT,
    status TEXT,
    first_time_found TEXT,
    last_time_checked TEXT,
    FOREIGN KEY (bank_id) REFERENCES banks (id)
);
"""

conn = create_connection(database_path)

if conn is not None:
    create_table(conn, sql_create_banks_table)
    create_table(conn, sql_create_appels_table)
    conn.close()
else:
    print("Error! cannot create the database connection.")

"Tables created successfully."
def insert_appel(conn, bank_id, keywords_found, status, first_time_found, last_time_checked):
    """
    Insert a new appel into the appels table.
    :param conn: Connection object
    :param bank_id: ID of the bank
    :param keywords_found: Keywords found in the scrape
    :param status: Status of the appel
    :param first_time_found: The first time the appel was found
    :param last_time_checked: The last time the appel was checked
    """
    sql = ''' INSERT INTO appels(bank_id, keywords_found, status, first_time_found, last_time_checked)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (bank_id, keywords_found, status, first_time_found, last_time_checked))
    conn.commit()
    return cur.lastrowid

def update_appel(conn, bank_id, keywords_found, status, last_time_checked):
    """
    Update an existing appel in the appels table.
    :param conn: Connection object
    :param bank_id: ID of the bank
    :param keywords_found: Keywords found in the scrape
    :param status: Status of the appel
    :param last_time_checked: The last time the appel was checked
    """
    sql = ''' UPDATE appels
              SET keywords_found = ? ,
                  status = ? ,
                  last_time_checked = ?
              WHERE bank_id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (keywords_found, status, last_time_checked, bank_id))
    conn.commit()