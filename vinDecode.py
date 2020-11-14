#Decodes Vin into year make model trim
import requests
from bs4 import BeautifulSoup

def decodeVin(vinNum):

	#Check if vin is invalid
	if len(vinNum) != 17:
		return ("ER-BadVin", " ", " ", " ")

	#Base URL
	url = "https://infotracer.com/vin-check/register/?vin=" + vinNum

	#Fetch Page
	page = requests.get(url)

	#Decode with Beautiful Soup
	soup = BeautifulSoup(page.content, 'html.parser')

	#Fetch ul class with name "rs-list sum" for summary info
	results = soup.find('ul', class_='rs-list sum')

	#Check for valid page
	if not results:
		return ("ER-BadVin", " ", " ", " ")

	#Fetch span class with name "val" for indiviual info
	vinValues = results.find_all('span', class_='val')

	#Assign values
	make = str(vinValues[0])[91:-11]
	model = str(vinValues[1])[91:-11]
	year = str(vinValues[2])[91:-11]
	trim =  str(vinValues[6])[91:-11]

	#Return for info
	return (year, make, model, trim)
