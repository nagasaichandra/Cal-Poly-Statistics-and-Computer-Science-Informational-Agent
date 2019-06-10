import requests
from bs4 import BeautifulSoup
import re
from ..database_connection import make_connection

def parse_courses():
    url = "http://catalog.calpoly.edu/collegesandprograms/collegeofengineering/computersciencesoftwareengineering/bscomputerscience/"
    myRequest = requests.get(url)
    soup = BeautifulSoup(myRequest.text, "html.parser")
    courses_tables = soup.find_all('table', attrs={'class': re.compile(r'sc_courselist')})

    courses_trs = courses_tables[0].find_all('tr')
    course_type = ""

    courses_list = []
    for tr in courses_trs:
        if "areaheader" in set(tr["class"]):
            course_type = tr.text
        else:
            course_name = tr.find("a", attrs={"class": re.compile("bubblelink code")})
            if course_name:
                course_dict = {}

                course_title = course_name["title"].replace("/CPE", "")
                course_area = re.search(r"([A-Z]+)", course_title).group(1).replace("'", "")
                course_number = re.search(r"\b[1-5][0-9]{2}\b", course_title).group()
                course_info = tr.find_all("td")
                course_units = 4
                course_name = ""
                for tag in course_info:
                    if not tag.has_attr("class"):
                        course_name = tag.text

                course_dict["course_area"] = course_area.replace("'", "")
                course_dict["num_units"] = course_units
                course_dict["support_type"] = course_type
                course_dict["course_name"] = course_name
                course_dict["course_number"] = course_number

                courses_list.append(course_dict)

    return courses_list

def delete_course_types():
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('''TRUNCATE TABLE course_types;''')
            connection.commit()
    finally:
        connection.close()

def ingest_course_types(course_types):
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            for course_type in course_types:
                cursor.execute('''INSERT INTO course_types (course_area, course_number, course_name, support_type)
                                VALUES (%s, %s, %s, %s);''', (course_type["course_area"],
                                                             course_type["course_number"],
                                                             course_type["course_name"],
                                                             course_type["support_type"]))
            connection.commit()
    finally:
        connection.close()



def scrape_electives():
    delete_course_types()
    list_courses = parse_courses()
    ingest_course_types(list_courses)

if __name__ == '__main__':
    delete_course_types()
    list_courses = parse_courses()
    ingest_course_types(list_courses)
