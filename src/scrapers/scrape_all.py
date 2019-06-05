from .catalogue_scraper import scrape_catalog
from .scrapeChangeMajor import scrapeChangeMajor
from .scrapeCSMinor import scrapecsminor
from .scrapeMasters import scrapeMasters
from .scrapeObjectivesandMissions import scrapeObjectivesandMissions
from .scrapeTransfer import scrapeTransfer


def scrape_all():
    """ Scrapes all the data sources and puts the data into the database """
    scrape_catalog()
    scrapeChangeMajor()
    scrapecsminor()
    scrapeMasters()
    scrapeObjectivesandMissions()
    scrapeTransfer()


if __name__ == '__main__':
    scrape_all()
