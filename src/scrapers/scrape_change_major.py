import requests, re, bleach, urllib3
from bs4 import BeautifulSoup

from src.database_connection import make_connection

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def filter_min_standards(line):
    exclude = ['[', '', 'Minimum Standards']
    if line not in exclude:
        return True
    else:
        return False


def filter_process(line):
    exclude = ['[', ']', '']
    if line not in exclude:
        return True
    else:
        return False


def ingest_change_major(data):
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('''DELETE FROM change_major_info;''')
            cursor.execute(
                '''INSERT INTO change_major_info (criteria, steps, minimum_gpa) VALUES ("%s", "%s", %s);''',
                (data['change-major-criteria'],
                 data['change-major-steps'],
                 float(data['minimum-gpa-change-major'])))
            connection.commit()
    finally:
        connection.close()


def scrape_change_major():
    final_dict = {}
    initial_list = []

    # obtain the content of the URL in HTML
    url = "https://eadvise.calpoly.edu/changing-majors-to-csc-se-or-cpe/"
    my_request = requests.get(url, verify=False)

    # Create a soup object that parses the HTML
    soup = BeautifulSoup(my_request.text, "html.parser")

    # Print the HTML Title
    # print("Page Title: ",soup.head.title.get_text())

    for changeRow in soup.find_all('div', attrs={"id": "mainLeftFull"}):
        initial_list.append(changeRow)

    initial_list = re.split(
        r"<h3><strong>Process<\/strong><\/h3>", str(initial_list))

    min_standards_list = str(bleach.clean(initial_list[0], tags=[], strip=True))
    process_list = str(bleach.clean(initial_list[1], tags=[], strip=True))

    min_standards_list = filter(
        filter_min_standards, min_standards_list.splitlines())
    process_list = filter(
        filter_process, process_list.splitlines())

    temp_list = '\n'.join(list(process_list))
    match_obj = re.search(r"\(all GPAs at least a (\d+\.\d+)\)", temp_list)

    # [change-major-steps], [change-major-criteria], [minimum-gpa-change-major]
    final_dict['change-major-criteria'] = '\n'.join(list(min_standards_list))
    final_dict['change-major-steps'] = temp_list
    final_dict['minimum-gpa-change-major'] = match_obj.group(1)

    ingest_change_major(final_dict)


if __name__ == "__main__":
    scrape_change_major()
