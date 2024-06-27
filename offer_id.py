import scrape_classes
import requests
import re
import time
from bs4 import BeautifulSoup


def extract_offer_id(offer_url):
    """Extracting offer ID from a otomoto.pl offer URL"""
    offer_url = offer_url.replace('-', ' ')
    offer_url = offer_url.replace('.', ' ')
    offer_url = offer_url.split()
    offer_id = offer_url[-2]
    return offer_id


def scrape_offer_id(list_page=1):
    """Retrieve a list of offer ID's from a selected, offer listing page"""
    offer_listing_class = scrape_classes.offer_listing_class
    if list_page == 1:
        url = "https://www.otomoto.pl/osobowe?search%5Border%5D=created_at_first%3Adesc"
    else:
        url = "https://www.otomoto.pl/osobowe?search%5Border%5D=created_at_first%3Adesc&page=" + str(list_page)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all(class_=offer_listing_class)

    ids = []
    for result in results:
        href = result.find('a').get('href')
        # Filtering out adds from actual offers.
        valid_url = re.search("^https://www.otomoto.pl", href)
        if valid_url:
            offer_id = extract_offer_id(href)
            ids.append(offer_id)
    return ids


def scrape_offer_id_range(list_page_range=1, delay=0):
    """Retrieve a list of offer ID's from a selected range of, offer listing pages"""
    ids = []
    for page in range(1, list_page_range + 1):
        page_ids = scrape_offer_id(page)
        # Join to ids without duplicates
        ids = ids + list(set(page_ids) - set(ids))
        time.sleep(delay)
    return ids
