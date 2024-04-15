# import requests
# from bs4 import BeautifulSoup

# # List of keywords to search for in the bank web pages
# KEYWORDS = [
#     'appel d’offre', 'offre d’emploi', 'marché public', 'soumission',
#     'Appel à candidature', 'appel à candidature', 'licitation'
# ]

# def fetch_webpage_content(url):
#     """
#     Fetch the content of a webpage.
#     :param url: URL of the webpage to scrape.
#     :return: The content of the webpage.
#     """
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Raise an error for bad responses
#         return response.text
#     except requests.RequestException as e:
#         print(f"Error fetching {url}: {e}")
#         return None

# def search_keywords_in_content(content):
#     """
#     Search for keywords in the provided content.
#     :param content: The content to search through.
#     :return: A list of found keywords.
#     """
#     found_keywords = []
#     for keyword in KEYWORDS:
#         if keyword.lower() in content.lower():
#             found_keywords.append(keyword)
#     return found_keywords

# def scrape_bank(url):
#     """
#     Scrape a bank's webpage and search for keywords.
#     :param url: URL of the bank's webpage.
#     :return: A list of found keywords in the webpage.
#     """
#     content = fetch_webpage_content(url)
#     if content:
#         return search_keywords_in_content(content)
#     return []

# # Example usage
# if __name__ == "__main__":
#     test_url = "https://www.atb.tn/ar/offres-emploi"
#     found_keywords = scrape_bank(test_url)
#     print(f"Found keywords in {test_url}: {found_keywords}")
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup

# List of keywords to search for in the bank web pages
# KEYWORDS = [
#     'appel d’offre','d'Appel d'Offre', 'offre d’emploi', 'marché public', 'soumission',
#     'Appel à candidature', 'appel à candidature', 'licitation'
# ]
KEYWORDS = [
    'appel d’offre', 'offre d’emploi','d\'Appel d\'Offres', 'marché public', 'soumission',
    'Appel à candidature', 'appel à candidature', 'licitation',
    'concours', 'offre publique', 'procurement', 'tender', 'bidding', 
    'solicitation', 'request for proposal', 'RFP', 'bid request', 
    'public tender', 'request for quotation', 'RFQ', 'contract opportunity',
    'procurement notice', 'government procurement', 'public contract',
    'invitation to bid', 'ITB', 'competitive bidding', 'contract notice',
    'procurement opportunity', 'e-procurement', 'online bidding',
    'electronic tendering', 'achats publics', 'consultation publique', 
    'avis de marché', 'marché à procédure adaptée', 'appel public à la concurrence'
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

def search_keywords_in_content(content):
    """
    Search for keywords in the provided content.
    :param content: The content to search through.
    :return: A list of found keywords.
    """
    found_keywords = []
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text().lower()
        for keyword in KEYWORDS:
            if keyword.lower() in text:
                found_keywords.append(keyword)
    return found_keywords

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
