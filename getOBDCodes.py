import requests
from bs4 import BeautifulSoup
import re
import sqlite3 as sql

def getCodes():

	#Update this to work for all of the following pages
	#https://www.obd-codes.com/trouble_codes/
	#https://www.obd-codes.com/body-codes
	#https://www.obd-codes.com/trouble_codes/obd-ii-c-chassis-codes.php
	#https://www.obd-codes.com/trouble_codes/obd-ii-u-network-codes.php
	#-----HERE------

	url2 = "https://www.obd-codes.com/body-codes"
	url3 = "https://www.obd-codes.com/trouble_codes/obd-ii-c-chassis-codes.php"
	url4 = "https://www.obd-codes.com/trouble_codes/obd-ii-u-network-codes.php"

	#Url for scraping

	listName = ["https://www.obd-codes.com/p00-codes", "https://www.obd-codes.com/trouble_codes/",
	"https://www.obd-codes.com/trouble_codes/obd-ii-c-chassis-codes.php", "https://www.obd-codes.com/trouble_codes/obd-ii-c-chassis-codes.php",
	"https://www.obd-codes.com/trouble_codes/obd-ii-u-network-codes.php"]
	for i in range(0,len(listName)):
		url = listName[i]

	#Fetch URL
	response = requests.get(url)
	#Parse HTML
	soup = BeautifulSoup(response.content, 'html.parser')
	#Grab list of all entries on page
	codes = soup.find_all('li')
	#Split into Numbers and Names
	codeNames = []
	codeNumbers = []
	for code in codes:
		code = str(code)[21:-9]
		if code.startswith('('):
			code = ''
		else:
			codeNum = code[:5]
			code = code[6:]
			codeNames.append(code)
			codeNumbers.append(codeNum)

	#Finalize list (Only for first page, will need to change for others)
	#-----HERE-----
	codeNames = codeNames[7:-1]
	codeNumbers = codeNumbers[7:-1]

	#Insert a check here for P listings only
	#----HERE-----DONE
	if codeNumbers[0] == 'P':
		print("P listing valid for scraping")
	#Send CodeNumber to page scraper
	for num in codeNumbers:
		codeDesc = getCodeInfo(num)
	else:
		print("NO")
		return False

	#Commit CodeNames, CodeNumbers, and CodeDesc to DB
	# --HERE--
	#with sql.connect("car_base.zip") as con:

def getCodeInfo(num):

	#base url
	url = "https://www.obd-data.com/" + num + ".html"
	print (url)
	#Fetch URL
	response = requests.get(url)

	#Parse HTML
	soup = BeautifulSoup(response.content, 'html.parser')

	#Grab list of all entries on page
	entry = soup.find('div', class_='entry-content')

	#Narrow down selection
	results = soup.find_all('span')

	#Check for content
	#----HERE----DONE
	test = soup.find_all(text=re.compile('Code Description'))
	if test:
		print("VALID PROBLEM CODE DETECTED")
		return True
	else:
		print("INVALID PROBLEM CODE, TRY AGAIN")
		return False

	#Filter html tags out
	codeDesc = []
	for result in results:
		result = str(result)[6:-7]
		codeDesc.append(result)

	#trim extra info
	codeDesc = codeDesc[1:10]
	print(codeDesc)
	return (codeDesc)


if __name__ == '__main__':
	getCodes()