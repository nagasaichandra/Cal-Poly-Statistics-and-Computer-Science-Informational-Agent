import requests
from bs4 import BeautifulSoup
import urllib3
import re
from ..database_connection import make_connection
import bleach

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def scrape_contact_main():
    """https://statistics.calpoly.edu/data-science-minor ===> DATA SCIENCE MINOR
    CSC Minor advisors contact available in a pdf at https://csc.calpoly.edu/static/media/uploads/computer_science_&_software_engineering_faculty_advisor_list_8-28-14.pdf
    Scrapes variables [[department-contact-info], [phone-number], [minor-advisors]]
    """
    global i
    url1 = "https://csc.calpoly.edu/contact/"
    my_request1 = requests.get(url1, verify=False)
    soup1 = BeautifulSoup(my_request1.text, "html.parser")
    url2 = "https://statistics.calpoly.edu/data-science-minor"
    my_request2 = requests.get(url2, verify=False)
    soup2 = BeautifulSoup(my_request2.text, "html.parser")
    final_dict = {}
    match = re.search(r'Contact Information\n(.*)\n(.*)', soup1.get_text())
    department_contact = match.group(1)
    department_office_hours = match.group(2)
    match = re.search(r'Phone: (\d\d\d-\d\d\d-\d\d\d\d) ', department_contact)
    final_dict['phone-number'] = match.group(1)
    final_dict['department-contact-info'] = department_contact
    final_dict['department-office-hours'] = department_office_hours
    minor_advisors = {}
    cs_advisors = ['Bellardo', 'Clements', 'Dekhtyar', 'Gharibyan', 'Haung', 'Kearns', 'Keen', 'Khosmood', 'Kurfess',
                   'Lupo', 'Nico', 'Peterson', 'Seng', 'Staley', 'Sueda']
    cs_minor_string = ''
    for i in cs_advisors:
        cs_minor_string + i
    match = re.search(r'Minor Advising\n(.*)', soup2.get_text())
    minor_advisors['ds-minor'] = match.group(1)
    final_dict['minor-advisors'] = minor_advisors
    # print(final_dict)
    return final_dict


def clean_html(string):
    return bleach.clean(string, tags=[], strip=True)


def scrape_level():
    url = "http://catalog.calpoly.edu/academicstandardsandpolicies/otherinformation/#AcademicMinors"
    my_request = requests.get(url, verify=False)
    soup = BeautifulSoup(my_request.text, "html.parser")
    final_dict = {}

    level_html = soup.find_all('p', attrs={"style": "margin-left:40px"})
    level = clean_html(level_html)
    level_list = (level.replace(',', '\n')).split('\n')
    # print(level_list)

    for entry in level_list:
        if entry.startswith(' Freshman'):
            match_obj = re.search(r'Freshman ................... (.*)', entry)
            final_dict['freshman'] = match_obj.group(1)
        elif entry.startswith('Sophomore'):
            match_obj = re.search(r'Sophomore................. (.*)', entry)
            final_dict['sophomore'] = match_obj.group(1)
        elif entry.startswith(' Junior'):
            match_obj = re.search(r' Junior ......................... (.*)', entry)
            final_dict['junior'] = match_obj.group(1)
        elif entry.startswith('Senior'):
            match_obj = re.search(r'Senior......................... (.*)\]$', entry)
            final_dict['senior'] = match_obj.group(1)

    print(final_dict)
    # TODO: add to database
    return final_dict


def ingest_level_units(level_units):
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            for level in level_units:
                cursor.execute(
                    '''INSERT INTO class_level_units VALUES ("%s", "%s");''' %
                    (level,
                     level_units[level])
                )
            cursor.commit()
    finally:
        connection.close()


def ingest_contact_basic(contacts):
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                '''INSERT INTO contact_basic VALUES ("%s", "%s", "%s", "%s");''' %
                (contacts['phone-number'],
                 contacts[
                     'department-contact-info'],
                 contacts[
                     'department-contact-info'],
                 contacts[
                     'department-office-hours']))
            cursor.commit()
    finally:
        connection.close()


def ingest_contact_minor_advisors(contacts):
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            for minor in contacts['minor-advisors']:
                cursor.execute(
                    '''INSERT INTO contact_minor_advisors VALUES ("%s", "%s");''' % (
                        minor, contacts['minor-advisors'][minor]))
                cursor.commit()
    finally:
        connection.close()


def remove_content():
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('''TRUNCATE TABLE contact_basic''')
            cursor.execute('''TRUNCATE TABLE contact_minor_advisors''')
            cursor.execute('''TRUNCATE TABLE class_level_units''')
            cursor.commit()
    finally:
        connection.close()


# scrape_contact_main()
def scrape_contact():
    remove_content()
    contacts = scrape_contact_main()
    ingest_contact_basic(contacts)
    ingest_contact_minor_advisors(contacts)
    level_units = scrape_level()
    ingest_level_units(level_units)


if __name__ == "__main__":
    # scrape_level()
    scrape_contact()
