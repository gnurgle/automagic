#Grabs recall information and output html insertable
import requests
from bs4 import BeautifulSoup

def fetchRecalls(year,make,model):

	#Base URL
	url = "https://autodetective.com/directory/" + str(year) + "/" + \
			make + "/" + model + "/"
	
	#Fetch Page
	page = requests.get(url)

	if response.status_code != 200:
		return ("No Recalls Found")

	#Decode with Beautiful Soup
	soup = BeautifulSoup(page.content, 'html.parser')

	#Fetch div id with name "rs-list sum" for summary info
	results = soup.find('div', {"id": "tab-04"})

	#Fetch just recal info
	output = results.find_all('div', class_="cf safety-recall")
	
	#Return for info
	return (results)

