import requests
from bs4 import BeautifulSoup
import re
from ..database_connection import make_connection

'''
division-level-units
icma-conditions
honors-gpa-list 
class-
'''

def parse_icma():
    url = "http://catalog.calpoly.edu/academicstandardsandpolicies/otherinformation/#ChangeofMajor"
    myRequest = requests.get(url)
    soup = BeautifulSoup(myRequest.text, "html.parser")
    tags = soup.find_all('p')
    icma = [tag.text for tag in tags[31: 39]]
    honors_text = tags[11].text.split('\n')
    honors_dict = {'Summa cum laude' : re.search(r'– ([1-4]\.[0-9]{3})', honors_text[0]).group(1),
                   'Magna cum laude' : re.search(r'– ([1-4]\.[0-9]{3})', honors_text[1]).group(1),
                   'Cum laude' : re.search(r'– ([1-4]\.[0-9]{3})', honors_text[2]).group(1)}

    return icma, honors_dict

def ingest_icma(icma):
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('''TRUNCATE TABLE ICMA;''')
            connection.commit()
        with connection.cursor() as cursor:
            cursor.execute('''INSERT INTO ICMA (icma_conditions) VALUES (%s);''', '\n'.join(icma))
            connection.commit()
    finally:
        connection.close()

def ingest_honors(honors_dict):
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('''TRUNCATE TABLE honors;''')
            connection.commit()
        with connection.cursor() as cursor:
            for honor_name in honors_dict.keys():
                cursor.execute('''INSERT INTO honors (honor_name, GPA) VALUES (%s, %s);''', (honor_name, honors_dict[honor_name]))
                connection.commit()
    finally:
        connection.close()

def ingest_levels():
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('''TRUNCATE TABLE division_levels;''')
            cursor.execute('''TRUNCATE TABLE class_levels;''')
            connection.commit()
        with connection.cursor() as cursor:
            cursor.execute('''INSERT INTO division_levels (division_level, num_units_lower, num_units_upper) VALUES ("lower", 0, 90);''')
            cursor.execute('''INSERT INTO division_levels (division_level, num_units_lower, num_units_upper) VALUES ("upper", 91, 250);''')
            cursor.execute('''INSERT INTO class_levels (class_level, num_units_lower, num_units_upper) VALUES ("freshman", 0, 45);''')
            cursor.execute('''INSERT INTO class_levels (class_level, num_units_lower, num_units_upper) VALUES ("sophmore", 46, 89);''')
            cursor.execute('''INSERT INTO class_levels (class_level, num_units_lower, num_units_upper) VALUES ("junior", 90, 134);''')
            cursor.execute('''INSERT INTO class_levels (class_level, num_units_lower, num_units_upper) VALUES ("senior", 135, 250);''')
            connection.commit()
    finally:
        connection.close()


def scrape_icma_honors():
    icma, honors_dict = parse_icma()
    ingest_icma(icma)
    ingest_honors(honors_dict)
    ingest_levels()


if __name__ == '__main__':
    scrape_icma_honors()