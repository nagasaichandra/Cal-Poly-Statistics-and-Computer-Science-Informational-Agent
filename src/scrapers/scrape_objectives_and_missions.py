import requests
from bs4 import BeautifulSoup
import urllib3
import re
from ..database_connection import make_connection


def scrapeObjectivesandMissions():
    """Scrapes variables [[CSSE-mission-statement], [major-PEOs], [major-learning-Outcomes-List], [GE-learning-outcomes], [major-Learning-Outcomes-List], [ms-learning-objectives]
    """
    urllib3.disable_warnings()
    url1 = "https://csc.calpoly.edu/about/"
    url2 = "https://csc.calpoly.edu/programs/"
    url3 = "http://catalog.calpoly.edu/generalrequirementsbachelorsdegree/#generaleducationtext"
    url4 = "http://catalog.calpoly.edu/collegesandprograms/collegeofengineering/computersciencesoftwareengineering/mscomputerscience/"
    myRequest1 = requests.get(url1, verify=False)
    soup1 = BeautifulSoup(myRequest1.text, "html.parser")
    myRequest2 = requests.get(url2, verify=False)
    soup2 = BeautifulSoup(myRequest2.text, "html.parser")
    myRequest3 = requests.get(url3, verify=False)
    soup3 = BeautifulSoup(myRequest3.text, "html.parser")
    myRequest4 = requests.get(url4, verify=False)
    soup4 = BeautifulSoup(myRequest4.text, "html.parser")

    major_peos = {}
    major_learning_outcomes_list = {}
    final_dict = {}

    match = re.search(r'Mission Statement (.*)\nEnrollment', soup1.get_text())
    final_dict['csse-mission-statement'] = match.group(1)

    match = re.search(r'(.*)\n(.*)\n(.*)\n(.*)\n\n\nComputer Science Student Learning Outcomes\n', soup2.get_text())
    cs_peo = list()
    for i in range(1, 5):
        cs_peo.append(match.group(i))
    major_peos['CSC'] = cs_peo

    match = re.search(
        r'At the time of graduation, students who major in Computer Science have:\n\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)',
        soup2.get_text())
    cs_learning_outcomes = list()
    for i in range(1, 12):
        cs_learning_outcomes.append(match.group(i))
    major_learning_outcomes_list['CSC'] = cs_learning_outcomes

    match = re.search(r'(.*)\n(.*)\n(.*)\n(.*)\n\nSoftware Engineering Student Learning Outcomes', soup2.get_text())
    se_peo = list()
    for i in range(1, 5):
        se_peo.append(match.group(i))
    major_peos['SE'] = se_peo
    se_learning_outcomes = list()

    match = re.search(
        r'At the time of graduation, students who major in Software Engineering have:\n\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n',
        soup2.get_text())
    for i in range(1, 12):
        se_learning_outcomes.append(match.group(i))
    major_learning_outcomes_list['SE'] = se_learning_outcomes
    final_dict['major-learning-outcomes-list'] = major_learning_outcomes_list
    final_dict['major-peos'] = major_peos

    match = re.search(
        r"After completing Cal Poly's General Education Program, students will be able to:\n\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)",
        soup3.get_text())
    ge_learning_outcomes = list()
    for i in range(1, 8):
        ge_learning_outcomes.append(match.group(i))
    final_dict['ge-learning-outcomes'] = ge_learning_outcomes

    match = re.search('Program Learning Objectives\n(.*)', soup4.get_text())
    ms_learning = match.group(1).split('. ')
    ms_learning_objectives = list()
    for i in ms_learning:
        if i != '':
            ms_learning_objectives.append(i)

    final_dict['ms-learning-objectives'] = ms_learning_objectives

    return final_dict


def ingest_objectives_and_missions(objectives):
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            print(objectives)
            cursor.execute(
                '''INSERT INTO mission_statement VALUES ("%s");''',
                (objectives['csse-mission-statement']))
            for major in objectives['major-learning-outcomes-list'].keys():
                cursor.execute(
                    '''INSERT INTO major_learning_outcomes VALUES (%s, "%s");''',
                    (major, objectives['major-learning-outcomes-list'][major]))
            for major in objectives['major-peos'].keys():
                cursor.execute(
                    '''INSERT INTO major_peos VALUES (%s, "%s");''',
                    (major, objectives['major-peos'][major]))
            cursor.execute('''INSERT INTO ge_learning_outcomes VALUES ("%s");''',
                           ''.join(objectives['ge-learning-outcomes']))
            connection.commit()
    finally:
        connection.close()


def remove_contents():
    connection = make_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('''TRUNCATE TABLE mission_statement;''')
            cursor.execute('''TRUNCATE TABLE major_learning_outcomes;''')
            cursor.execute('''TRUNCATE TABLE major_peos;''')
            cursor.execute('''TRUNCATE TABLE ge_learning_outcomes;''')
            connection.commit()
    finally:
        connection.close()


def scraper_objectives():
    remove_contents()
    objectives = scrapeObjectivesandMissions()
    ingest_objectives_and_missions(objectives)


if __name__ == "__main__":
    scraper_objectives()
    # print(scrapeObjectivesandMissions())
