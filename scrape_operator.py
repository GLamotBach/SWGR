import os
import time
import scraper_otomoto
import offer_id


def scrape_batch(offers_to_scrap, delay=0):
    """Function for handling the whole scraping operation."""
    number_of_list_pages = offers_to_scrap // 32
    if offers_to_scrap % 32 != 0:
        number_of_list_pages += 1
    ids_to_check = offer_id.scrape_offer_id_range(number_of_list_pages, delay)
    print(f"Retrieved {len(ids_to_check)} offer ID's.")

    # Checking if scraped offer ID aren't already in dataset.
    checked_ids = []
    offers_in_database = scraper_otomoto.offers_in_database()
    for i in range(len(ids_to_check)):
        if scraper_otomoto.check_if_not_collected(ids_to_check[i], offers_in_database):
            checked_ids.append(ids_to_check[i])
    duplicated_offers = len(ids_to_check) - len(checked_ids)
    print(f"ID's validated: {len(checked_ids)}")

    # Scraping the valid offers.
    offer_number = 1
    failed_scrapes = 0
    for offer in checked_ids:
        os.system('cls')
        print(f"Scraping offer: {offer_number}/{len(checked_ids) - failed_scrapes}: {offer}")
        try:
            scraper_otomoto.collect_offer(offer)
        except (KeyError, AttributeError) :
            failed_scrapes += 1
            continue
        time.sleep(delay)
        offer_number += 1

    # Scraping report
    os.system('cls')
    print("Scraping completed")
    print(f"{offer_number} - Successfully added")
    if failed_scrapes > 0:
        print(f"{failed_scrapes} - Attempts failed")
    if duplicated_offers > 0:
        print(f"{duplicated_offers} - Offers already in database")


if __name__ == "__main__":
    os.system('cls')
    print("SWGR - otomoto.pl scraper")
    batch = int(input("How much offers to scrap ?\n"))
    scrape_batch(batch, delay=0.1)







