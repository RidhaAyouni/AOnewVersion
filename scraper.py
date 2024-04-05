import requests
from bs4 import BeautifulSoup

# List of keywords to search for in the bank web pages
KEYWORDS = [
    'appel d’offre', 'offre d’emploi', 'marché public', 'soumission',
    'Appel à candidature', 'appel à candidature', 'licitation'
]

def fetch_webpage_content(url):
    """
    Fetch the content of a webpage.
    :param url: URL of the webpage to scrape.
    :return: The content of the webpage.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def search_keywords_in_content(content):
    """
    Search for keywords in the provided content.
    :param content: The content to search through.
    :return: A list of found keywords.
    """
    found_keywords = []
    for keyword in KEYWORDS:
        if keyword.lower() in content.lower():
            found_keywords.append(keyword)
    return found_keywords

def scrape_bank(url):
    """
    Scrape a bank's webpage and search for keywords.
    :param url: URL of the bank's webpage.
    :return: A list of found keywords in the webpage.
    """
    content = fetch_webpage_content(url)
    if content:
        return search_keywords_in_content(content)
    return []

# Example usage
if __name__ == "__main__":
    test_url = "https://www.atb.tn/ar/offres-emploi"
    found_keywords = scrape_bank(test_url)
    print(f"Found keywords in {test_url}: {found_keywords}")
