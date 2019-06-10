import requests
import re
import bleach
import urllib3
from bs4 import BeautifulSoup
from ..database_connection import make_connection

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def scrape_degrees():
    final_list = []

    # TODO: this is just for demo
    final_list = [('B.S. Computer Science', 'https://csc.calpoly.edu/programs/bs-computer-science/'),
     ('B.S. Software Engineering',
      'https://csc.calpoly.edu/programs/bs-software-engineering/'),
     ('M.S. Computer Science', 'https://csc.calpoly.edu/programs/ms-computer-science/'),
     ('Blended B.S. + M.S.', 'https://csc.calpoly.edu/programs/blended-bs-ms/'),
     ('Minor in Computer Science',
      'https://csc.calpoly.edu/programs/minor-computer-science/'),
     ('Computing for Interactive Arts Minor',
      'https://csc.calpoly.edu/programs/computing-interactive-arts-minor/'),
     ('Cross Disciplinary Studies Minor in Data Science', 
     'https://csc.calpoly.edu/programs/cross-disciplinary-studies-minor-data-science/')]


    remove_content()
    ingest_degrees(final_list)

def remove_content():
    """Removes all rows from the courses table.  """
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('''TRUNCATE TABLE degrees;''')
            connection.commit()
    finally:
        connection.close()


def ingest_degrees(degrees):
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            for program, link in degrees:
                cursor.execute(
                    'INSERT INTO degrees VALUES (%s, %s);',
                    (program, link))
                connection.commit()
    finally:
        connection.close()

if __name__ == "__main__":
    scrape_degrees()
