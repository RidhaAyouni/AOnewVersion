import sqlite3
from sqlite3 import Error

DOMAIN_KEYWORDS = [
    'Banque', 'Finance', 'Finance de marché', 'Services financiers', 'Marchés financiers',
    'Dépositaire', 'Custody', 'Gestion d’actifs', 'OPCVM', 'Gestion de portefeuille',
    'Post-marché', 'Post-trade', 'Collatéral', 'SWIFT', 'Actions', 'Obligations',
    'Opérations titres', 'Solution', 'Logiciel', 'Système d\'information',
    'Maitrise d\'ouvrage', 'AMOA', 'Institut financier', 'Finance Marché Financier',
    'ECMS', 'MOA titres', 'Business Analyst', 'FusionRisk',
    'Assistance à maîtrise d\'ouvrage', 'Product Owner', 'Consultant fonctionnel',
    'Scrum', 'Agile', 'GBCP', 'Chorus', 'Megara', 'Migration',
    'Intégration', 'Digital'
]

database_path = 'banks_appel_doffre.db'

def create_connection(db_file):
    """Create a database connection to a SQLite database"""
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        return None

def create_table(conn):
    """Create keywords table"""
    sql_create_table = """
    CREATE TABLE IF NOT EXISTS keywords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword TEXT NOT NULL UNIQUE
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql_create_table)
        conn.commit()
    except Error as e:
        print(e)

def insert_keywords(conn, keywords):
    """Insert a list of keywords into the keywords table"""
    try:
        cursor = conn.cursor()
        cursor.executemany("INSERT OR IGNORE INTO keywords (keyword) VALUES (?)",
                           [(k,) for k in keywords])
        conn.commit()
    except Error as e:
        print(e)

# Execution
conn = create_connection(database_path)
if conn is not None:
    create_table(conn)
    insert_keywords(conn, DOMAIN_KEYWORDS)
    conn.close()
    print("Keywords inserted successfully.")
else:
    print("Error! Cannot create the database connection.")
