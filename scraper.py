
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup


# KEYWORDS = [
#     'appel d’offre', 'offre d’emploi','d\'Appel d\'Offres', 'marché public', 'soumission',
#     'Appel à candidature', 'appel à candidature', 'licitation',
#     'concours', 'offre publique', 'procurement', 'tender', 'bidding',
#     'solicitation', 'request for proposal', 'RFP', 'bid request',
#     'public tender', 'request for quotation', 'RFQ', 'contract opportunity',
#     'procurement notice', 'government procurement', 'public contract',
#     'invitation to bid', 'ITB', 'competitive bidding', 'contract notice',
#     'procurement opportunity', 'e-procurement', 'online bidding',
#     'electronic tendering', 'achats publics', 'consultation publique',
#     'avis de marché', 'marché à procédure adaptée', 'appel public à la concurrence'
# ]
KEYWORDS = [
    'appel d’offre', 'offre d’emploi', 'd\'Appel d\'Offres', 'marché public', 'soumission',
    'Appel à candidature', 'appel à candidature', 'licitation',
    'concours', 'offre publique', 'procurement', 'tender', 'bidding',
    'solicitation', 'request for proposal', 'RFP', 'bid request',
    'public tender', 'request for quotation', 'RFQ', 'contract opportunity',
    'procurement notice', 'government procurement', 'public contract',
    'invitation to bid', 'ITB', 'competitive bidding', 'contract notice',
    'procurement opportunity', 'e-procurement', 'online bidding',
    'electronic tendering', 'achats publics', 'consultation publique',
    'avis de marché', 'marché à procédure adaptée', 'appel public à la concurrence',
    'RFI', 'Avis d\'appel d\'offres', 'Avis de consultation', 'Avis de reports appel d\'offres'
]

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


def setup_session():
    """
    Set up a requests session with retries and a timeout.
    """
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session

def fetch_webpage_content(url):
    """
    Fetch the content of a webpage with error handling for SSL and timeouts.
    """
    session = setup_session()
    try:
        response = session.get(url, timeout=10, verify=False)  # verify=False bypasses SSL verification
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# def search_keywords_in_content(content):
#     """
#     Search for keywords in the provided content.
#     :param content: The content to search through.
#     :return: A list of found keywords.
#     """
#     found_keywords = []
#     if content:
#         soup = BeautifulSoup(content, 'html.parser')
#         text = soup.get_text().lower()
#         for keyword in KEYWORDS :
#             if keyword.lower() in text:
#                 found_keywords.append(keyword)
#     return found_keywords
from bs4 import BeautifulSoup


def search_keywords_in_content(content, general_keywords=KEYWORDS, domain_keywords=DOMAIN_KEYWORDS):
    """
    Search for domain-specific keywords in the content only if at least one general keyword is found.

    :param content: HTML or plain text content to search through.
    :param general_keywords: List of general keywords to look for first.
    :param domain_keywords: List of domain-specific keywords to return if any general keyword is found.
    :return: A list of found domain-specific keywords.
    """
    found_domain_keywords = []

    if content:
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text().lower()

        # Check if at least one general keyword exists
        if any(keyword.lower() in text for keyword in general_keywords):
            # Search for domain-specific keywords
            for keyword in domain_keywords:
                if keyword.lower() in text:
                    found_domain_keywords.append(keyword)

    return found_domain_keywords


def scrape_bank(url):
    """
    Scrape a bank's webpage and search for keywords.
    :param url: URL of the bank's webpage.
    :return: A list of found keywords in the webpage.
    """
    content = fetch_webpage_content(url)
    return search_keywords_in_content(content)

# Example usage
if __name__ == "__main__":
    test_url = "https://www.atb.tn/ar/offres-emploi"
    found_keywords = scrape_bank(test_url)
    print(f"Found keywords in {test_url}: {found_keywords}")
