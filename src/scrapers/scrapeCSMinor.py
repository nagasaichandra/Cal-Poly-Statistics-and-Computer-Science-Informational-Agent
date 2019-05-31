import requests
from bs4 import BeautifulSoup
import urllib3
import re


def scrapecsminor():
	"""Scrapes variables [minor-required-units], [minor-approved-elective-units], [minor-general-requirements], [minor-steps], [required-minor-courses], [minor-application-link]
	"""
	urllib3.disable_warnings() 
	url1 = "https://eadvise.calpoly.edu/minors/computer-science-minor/"
	myRequest = requests.get(url1, verify=False)
	soupobj = BeautifulSoup(myRequest.text,"html.parser")
	pars_in_page = soupobj.find_all('li')
	required_minor_courses = list()
	for i in pars_in_page:
		some_list = str(i.contents[0])
		match = re.findall(r'(\w\w\w\s[0-5][0-9][0-9])\s\w', some_list)	
		if match != []:		
			required_minor_courses.append(match[0])
	final_dict = {}
	final_dict['required-minor-courses'] = required_minor_courses
	pars_in_page = soupobj.find_all('h2')
	final_dict['minor-steps'] = re.findall(r'(Step [0-9]\: .*)',soupobj.get_text())	
		
	match = re.search(r'grade point average must be a ([0-9]\.[0-9][0-9]) or higher', soupobj.get_text())
	final_dict['minimum-gpa-minor'] = match.group(1)
	match = re.search(r'Step 2: Meet CSC Minor Prerequisites\n(.*)',soupobj.get_text())
	final_dict['minor-prerequisites'] = match.group(1)	
	a_matches = soupobj.find('a', string="CSC Minor Interest Form")
	final_dict['minor-application-link'] = a_matches['href']
	print(soupobj.get_text())
	match = re.search(r'Required Courses \(([0-9][0-9]) units\)', soupobj.get_text())
	if match:
		final_dict['minor-required-units'] = match.group(1)
	match = re.search(r'Approved Electives \(([0-9][0-9]) units\)', soupobj.get_text())
	if match:
		final_dict['minor-approved-elective-units'] = match.group(1)

	url2 = "http://catalog.calpoly.edu/academicstandardsandpolicies/otherinformation/#AcademicMinors"
	myRequest2 = requests.get(url2, verify=False)
	soupobj2 = BeautifulSoup(myRequest2.text,"html.parser")
	match = re.search(r'Requirements for the minor:\n\n(.*)\n(.*)\n(.*)\n(.*)', soupobj2.get_text())
	if match:
		final_dict['division-units'] = match.group(1)
	general_requirements = list()
	for i in range(1,5):
		general_requirements.append(match.group(i))
	final_dict['minor-general-requirements'] = general_requirements
	final_dict['minor-flowchart-link'] = 'https://flowcharts.calpoly.edu/'
	return final_dict



if __name__ == "__main__":
	print(scrapecsminor())

