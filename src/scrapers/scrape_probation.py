import requests
import re
import bleach
import urllib3
from bs4 import BeautifulSoup
from ..database_connection import make_connection
from ..data_sustainer import DataSustainer



# from ..database_connection import connection

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
    Scrapes:
    [probation-criteria]
    [disqualification-criteria]
"""


def clean_html(string):
    return bleach.clean(string, tags=[], strip=True)


def scrape_probation():
    final_dict = {}
    probation_html = []

    # obtain the content of the URL in HTML
    url = "https://advising.calpoly.edu/academic-probation-support"

    my_request = requests.get(url, verify=False)

    # Create a soup object that parses the HTML
    soup = BeautifulSoup(my_request.text, "html.parser")

    # gather data
    for probation_row in soup.find_all('div', attrs={"class": "field-item even"}):
        disqualificaiton_html = probation_row.find_all('td')
        probation_html.append(probation_row)

    match_probation = re.search(r'What is academic probation\?\n(.*)',
                                clean_html(probation_html[0]))
    match_disqualification = re.search(r'What is disqualification\?\n(.*)',
                                       clean_html(probation_html[0]))

    probation_limits = "\n".join(list(map(clean_html, disqualificaiton_html)))

    final_dict['probation-criteria'] = match_probation.group(1)
    final_dict['disqualification-criteria'] = match_disqualification.group(1) + "\n" + probation_limits
    return final_dict


def ingest_probation(probation):
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO probation VALUES ("%s", "%s");', 
                (probation['probation-criteria'],
                probation['disqualification-criteria']))
            connection.commit()
    finally:
        connection.close()


def remove_probation():
    '''Removes all rows from the courses table.  '''
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('''TRUNCATE TABLE probation;''')
            connection.commit()
    finally:
        connection.close()

if __name__ == "__main__":
    final = scrape_probation()
    # data_sustainer = DataSustainer()
    # data_sustainer.create_tables(filename="createTableProbation.sql")
    remove_probation()
    ingest_probation(final)
