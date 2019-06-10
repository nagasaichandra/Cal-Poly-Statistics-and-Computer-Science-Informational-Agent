import time
from sys import stderr
from .scrape_courses import scrape_catalog
from .scrape_change_major import scrape_change_major
from .scrape_cs_minor import scrape_cs_minor
from .scrape_masters import scrape_masters
from .scrape_objectives_and_missions import scraper_objectives
from .scrape_transfer import scrape_transfer
from .scrape_masters import scrape_blended
from .scrape_contact import scrape_contact
from .scrape_probation import scrape_probation
from .scrape_courses_requirements import scrape_electives
from .scrape_flowchart_links import flowchart_links
from .scrape_ge import scrape_ges
from .scrape_icma import scrape_icma_honors


scraping_functions = [scrape_catalog,
    scrape_change_major,
    scrape_cs_minor,
    scrape_masters,
    scraper_objectives,
    scrape_transfer,
    scrape_blended,
    scrape_contact,
    scrape_probation,
    scrape_electives,
    flowchart_links,
    scrape_ges,
    scrape_icma_honors]


def scrape_all():
    """ Scrapes all the data sources and puts the data into the database """
    print("Running all scrapers.")
    start_time = time.time()
    for scraping_function in scraping_functions:
        try:
            scraping_function()
        except Exception as exception:
            print('Failed to run scrapper', scraping_function, file=stderr)
            print(exception, file=stderr)
    print("Scraping finished in", time.time() - start_time, 'seconds.')


if __name__ == '__main__':
    scrape_all()
