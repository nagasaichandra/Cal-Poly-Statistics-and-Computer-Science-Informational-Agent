import requests
import re
import bleach
import urllib3
from bs4 import BeautifulSoup
from ..database_connection import make_connection

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
    Scrapes:
        [transfer-min-units]
        [transfer-articulate-courses]
        [CSSE-transfer-guidelines]
        [major-transfer-course-list]
"""


def get_tag(row, string):
    ret_list = []
    for single in row:
        if single.find(string) is not None and single.find(string) != -1:
            ret_list.append(single.find(string))
    return ret_list


def get_tag_attrs(row, string, attr, field):
    ret_list = []
    for single in row:
        if single.find(string, attrs={str(attr): str(field)}) is not None and single.find(string, attrs={
            str(attr): str(field)}) != -1:
            ret_list.append(single.find(string, attrs={str(attr): str(field)}))
    return ret_list


def clean_html(string):
    return bleach.clean(string, tags=[], strip=True)


def scrape_transfer():
    final_dict = {}
    articulates_html = []

    # obtain the content of the URL in HTML
    url = "https://admissions.calpoly.edu/computer-science.html"

    my_request = requests.get(url, verify=False)

    # Create a soup object that parses the HTML
    soup = BeautifulSoup(my_request.text, "html.parser")

    # gather data
    for transfer_row in soup.find_all('div', attrs={"class": "field-item even"}):
        transfer_units_html = get_tag(transfer_row, 'u')
        articulates_html = transfer_row.find_all('td', attrs={"width": "700"})
        general_guides_html = transfer_row.find_all('p')
        bullets_html = transfer_row.find_all('li')

    # clean up and split courses
    articulates = "\n".join(list(map(clean_html, articulates_html)))
    articulates = re.split(
        r'Major Related 1\*', str(articulates))

    match_obj = re.search(r'(Selection.*alone\.)',
                          "\n".join(list(map(clean_html, general_guides_html))))

    final_dict['transfer-min-units'] = clean_html(transfer_units_html[0])
    final_dict['transfer-articulate-courses'] = articulates[1]
    final_dict['CSSE-transfer-guidelines'] = match_obj.group(1)
    # + "\n" + clean_html(bullets_html)
    final_dict['major-transfer-course-list'] = "Major Related 1*\n" + articulates[0]
    
    remove_content()
    ingest_transfer(final_dict)

    return final_dict


def ingest_transfer(transfer):
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO transfers VALUES ("%s", "%s", "%s", "%s");',
                (transfer['transfer-min-units'],
                    transfer[
                        'transfer-articulate-courses'],
                    transfer[
                        'CSSE-transfer-guidelines'],
                    transfer[
                        'major-transfer-course-list']))
            connection.commit()
    finally:
        connection.close()



def remove_content():
    """Removes all rows from the courses table.  """
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('''TRUNCATE TABLE transfers;''')
            connection.commit()
    finally:
        connection.close()


if __name__ == "__main__":
    scrape_transfer()
    # print(final['transfer-min-units'])
    # print(final['transfer-articulate-courses'])
    # print(final['CSSE-transfer-guidelines'])
    # print(final['major-transfer-course-list'])
    # data_sustainer = DataSustainer()
    # data_sustainer.create_tables(filename="createTableTransfer.sql")
    # remove_content()
    # ingest_transfer(final)
