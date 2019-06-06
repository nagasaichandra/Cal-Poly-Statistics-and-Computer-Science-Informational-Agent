import requests
from bs4 import BeautifulSoup
import urllib3
import re


def scrapeContact():
	"""
		https://statistics.calpoly.edu/data-science-minor ===> DATA SCIENCE MINOR
		CSC Minor advisors contact available in a pdf at https://csc.calpoly.edu/static/media/uploads/computer_science_&_software_engineering_faculty_advisor_list_8-28-14.pdf
		Scrapes variables [[department-contact-info], [phone-number], [minor-advisors]]
	"""

	
	urllib3.disable_warnings()
	
	url1 = "https://csc.calpoly.edu/contact/"
	myRequest1 = requests.get(url1, verify=False)
	soup1 = BeautifulSoup(myRequest1.text,"html.parser")
	
	url2 = "https://statistics.calpoly.edu/data-science-minor"
	myRequest2 = requests.get(url2, verify=False)
	soup2 = BeautifulSoup(myRequest2.text,"html.parser")
	
	final_dict = {}
	match = re.search(r'Contact Information\n(.*)\n(.*)', soup1.get_text())
	department_contact = match.group(1)
	department_office_hours = match.group(2)
	match = re.search(r'Phone: (\d\d\d\-\d\d\d\-\d\d\d\d) ', department_contact)
	final_dict['phone-number'] = match.group(1)
	final_dict['department-contact-info'] = department_contact
	final_dict['department-office-hours'] = department_office_hours
	
	minor_advisors = {}
	minor_advisors['cs-minor'] = ['Bellardo', 'Clements', 'Dekhtyar', 'Gharibyan', 'Haung', 'Kearns', 'Keen', 'Khosmood', 'Kurfess', 'Lupo', 'Nico', 'Peterson', 'Seng', 'Staley', 'Sueda']
	
	match = re.search(r'Minor Advising\n(.*)', soup2.get_text())
	minor_advisors['ds-minor'] = match.group(1)
	final_dict['minor-advisors'] = minor_advisors
	 
	
if __name__ == "__main__":
	scrapeContact()

