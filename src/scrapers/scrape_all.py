from .catalogue_scraper import scrape_catalog
from .scrapeChangeMajor import scrapeChangeMajor
from .scrapeCSMinor import scrapecsminor
from .scrape_masters import scrape_masters
from .scrapeObjectivesandMissions import scrapeObjectivesandMissions
from .scrapeTransfer import scrapeTransfer


def scrape_all():
    """ Scrapes all the data sources and puts the data into the database """
    scrape_catalog()
    scrapeChangeMajor()
    scrapecsminor()
    scrape_masters()
    scrapeObjectivesandMissions()
    scrapeTransfer()


if __name__ == '__main__':
    scrape_all()
