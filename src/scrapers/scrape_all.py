import time
from .scrape_courses import scrape_catalog
from .scrape_change_major import scrape_change_major
from .scrape_cs_minor import scrape_cs_minor
from .scrape_masters import scrape_masters
from .scrape_objectives_and_missions import scrapeObjectivesandMissions
from .scrape_transfer import scrape_transfer
from .scrape_masters import scrape_blended
from .scrape_contact import scrape_contact
from .scrape_probation import scrape_probation


scraping_functions = [scrape_catalog,
    scrape_change_major,
    scrape_cs_minor,
    scrape_masters,
    scrapeObjectivesandMissions,
    scrape_transfer,
    scrape_blended,
    scrape_contact,
    scrape_probation]


def scrape_all():
    """ Scrapes all the data sources and puts the data into the database """
    print("Running all scrapers.")
    start_time = time.time()
    for scraping_function in scraping_functions:
        try:
            scraping_function()
        except:
            print('Failed to run scrapper', scraping_function)
    print("Scraping finished in", time.time() - start_time, 'seconds.')


if __name__ == '__main__':
    scrape_all()
