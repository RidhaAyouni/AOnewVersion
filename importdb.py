# importdb.py
import sqlite3
from database import create_connection
# List of keywords to search for in the bank web pages
KEYWORDS = [
    'appel d’offre', 'offre d’emploi', 'marché public', 'soumission',
    'Appel à candidature', 'appel à candidature', 'licitation'
]

# List of banks and their associated URLs to be monitored
BANK_DATA = [
    ("ALUBAF INTERNATIONAL BANK-TUNIS", "http://www.alubaf.com.tn/?q=fr/search/node/actualit%C3%A9s"),
    ("ATB", "https://www.atb.tn/ar/offres-emploi"),
    ("BFT", "https://www.bftunis.com/actualit%C3%A9s"),
    ("BNA", "http://www.bna.tn/fr/appels-d-offres-resultats.832.html"),
    ("Attijari Bank", "https://www.attijariwafabank.com/fr/recherche?search_api_fulltext=appel%20d%27offre"),
    ("BT", "https://www.bt.com.tn/News/26054"),
    ("AMEN BANK", "https://www.stbfinance.com.tn/amen-bank-appel-candidature"),
    ("BIAT", "https://www.biat.com.tn/search/content?keys=appel+d%27offre"),
    ("STB", "https://www.stb.com.tn/fr/actualites/"),
    ("UBCI", "https://ubci.csod.com/ux/ats/careersite/1/home?c=ubci&lang=fr-FR"),
    ("UIB", "https://www.stbfinance.com.tn/uib-appel-candidature"),
    ("BH BANK", "https://www.bhbank.tn/publications"),
    ("BTK", "https://www.btknet.com/site/fr/news_details.php?id_article=218&id_news=7"),
    ("TSB", "https://www.tsb.com.tn/fr/recherche?recherche=Appel+d%27offre"),
    ("QNB", "https://www.qnb.com.tn/fr/derniers-actualites-rapports.html"),
    ("BTE", "https://www.bte.com.tn/en/recherche?searchword=actualit%C3%A9&searchphrase=all"),
    ("BanqueZitouna", "https://www.banquezitouna.com/fr/actualites-et-evenements/appel-candidatures-administrateurs-independants"),
    ("BTL", "https://btl.tn/actualites/"),
    ("BTS", "https://www.bts.com.tn/?s=appel+d%27offre"),
    ("BFMPE", "https://bfpme.com.tn/?page_id=6359"),
    ("ALBARAKA BANK", "https://albaraka.com.tn/fr/actualites?title=Appel+d%27offre&field_theme_target_id=All"),
    ("WIFAK BANK", "https://managers.tn/2022/07/07/wifak-bank-lance-un-appel-a-candidature-pour-un-administrateur-independant/"),
    ("North Africa International Bank", "http://www.naibbank.com/index.php?option=com_search&Itemid=99999999&searchword=appel+d%27offre&submit=Recherche&searchphrase=any&ordering=newest"),
    ("S E R E P T", "https://www.serept.com.tn/Fr/recherche_57_36?q=Appel+d%27offre"),
    ("Milleis Banque", "https://www.milleis.fr/actualites-de-notre-maison?page=1")
]


database_path = 'banks_appel_doffre.db'

def insert_bank(conn, bank):
    """
    Insert a new bank into the banks table
    :param conn: Connection object
    :param bank: A tuple (name, url) representing bank details
    :return: bank id
    """
    sql = ''' INSERT INTO banks(name,url)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, bank)
    conn.commit()
    return cur.lastrowid

def import_banks(bank_data):
    """
    Import bank data into the database
    :param bank_data: A list of tuples (name, url) representing bank details
    """
    conn = create_connection(database_path)
    if conn is not None:
        with conn:
            for bank in bank_data:
                # Check if the bank already exists
                cur = conn.cursor()
                cur.execute("SELECT * FROM banks WHERE name=? AND url=?", bank)
                entry = cur.fetchone()
                if entry is None:
                    insert_bank(conn, bank)
    else:
        print("Error! cannot create the database connection.")

# Execute the import function
if __name__ == "__main__":
    import_banks(BANK_DATA)
