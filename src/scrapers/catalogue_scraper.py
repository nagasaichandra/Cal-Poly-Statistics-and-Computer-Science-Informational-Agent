import os, sys, random, requests
from bs4 import BeautifulSoup
import re

import sys
sys.path.append('../')
from ..database_connection import connection

def parse_course(class_tag):
	''' This function requires a tag for each class block and it returns 
	a dictionary of the attributes of the class passed.'''
	course_dict = {}
	course_complete = class_tag.find('strong').text
	
	course_name_re = re.search(r'[0-9]{3}\. ([^.\n]*)\.',course_complete)
	if course_name_re:
		course_name = course_name_re.group(1)
		course_dict['course_name'] = course_name
	
	course_num_re = re.search(r'([1-5][0-9][0-9])', course_complete)
	if course_num_re:
		course_num = course_num_re.group(1)
		course_dict['course_num'] = course_num
	
	units_text = class_tag.find('span', attrs = {'class': re.compile('courseblockhours')}).text
	units_re = re.search(r'([1-9]+)', units_text)
	# need to fix: some classes have units listed as a range.
	if units_re:
		units_num = units_re.group(1)
		course_dict['units'] = units_num
	seasons = class_tag.find('p', attrs = {'class': re.compile('noindent')}.text 
	
	return course_dict

def parse_courses():
	url = "http://catalog.calpoly.edu/coursesaz/csc/"
	myRequest = requests.get(url)
	soup = BeautifulSoup(myRequest.text, "html.parser")
	courses = soup.find_all('p', attrs = {'class' : re.compile('courseblocktitle')})
	courses_dicts = list(map(parse_course, courses))
	return courses_dicts

def ingest_courses(courses):
	with connection.cursor() as cursor:
		for course_dict in courses:
			cursor.execute('''INSERT INTO course VALUES (%s, "%s", "%s", %s);'''%(int(course_dict['course_num']),'CSCE', course_dict['course_name'], int(course_dict['units'])))
		connection.commit()


def remove_content():
	'''Removes all rows from the courses table.  '''
	with connection.cursor() as cursor:
		cursor.execute('''DELETE FROM course;''')
		connection.commit()

if __name__ == '__main__':
	courses = parse_courses()
	remove_content()
	ingest_courses(courses)	
