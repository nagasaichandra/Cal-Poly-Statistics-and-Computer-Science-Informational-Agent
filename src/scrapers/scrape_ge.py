import requests
from bs4 import BeautifulSoup
import re
from ..database_connection import make_connection


def parse_ge_age():
    url = "https://ge.calpoly.edu/content/ge-requirements-and-courses"
    myRequest = requests.get(url)
    soup = BeautifulSoup(myRequest.text, "html.parser")
    ge_reqs = soup.find('main')
    print(ge_reqs.find_all('ul'))

parse_ge_age()

'''

'''