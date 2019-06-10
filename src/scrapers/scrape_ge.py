import requests
from bs4 import BeautifulSoup
import re
from ..database_connection import make_connection

'''
ge-area-course-names, - 
ge-area-list, - 
ge-area-subject, - 
ge-requirements - 
'''
def parse_ge_age():
    url = "https://ge.calpoly.edu/content/ge-requirements-and-courses"
    myRequest = requests.get(url)
    soup = BeautifulSoup(myRequest.text, "html.parser")
    ge_tags = soup.find('main').find_all('ul')
    ge_areas = ge_tags[0].find_all('li')
    ge_area_names = {}
    ge_requirements = []
    for ge_area in ge_areas:
        area_name = re.search(r'([ABCEF])\)', ge_area.text).group(1)
        area_subject = re.search(r'(.*?)\(', ge_area.text).group(1)
        ge_area_names[area_name] = area_subject

    ge_req_tags = ge_tags[1].find_all('li')
    for ge_re in ge_req_tags:
        ge_requirements.append(ge_re.text)

    return ge_requirements, ge_area_names


def ingest_ge(ge_reqs, ge_area_names):
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('''TRUNCATE TABLE ge_requirements;''')
            cursor.execute('''TRUNCATE TABLE ge_subjects;''')
            connection.commit()
        with connection.cursor() as cursor:
            cursor.execute('''INSERT INTO ge_requirements (ge_requirements) VALUES (%s);''', '\n'.join(ge_reqs))
            for area in ge_area_names.keys():
                cursor.execute('''INSERT INTO ge_subjects (ge_letter, ge_subject) VALUES (%s, %s);''',
                               (area, ge_area_names[area]))
            connection.commit()
    finally:
        connection.close()


def scrape_ges():
    ge_reqs, ge_names = parse_ge_age()
    ingest_ge(ge_reqs, ge_names)


