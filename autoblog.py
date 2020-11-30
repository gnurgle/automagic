#Grabs image, pros and cons, and review
import requests
from bs4 import BeautifulSoup

def fetchReview(year,make,model):

	#Base URL
	baseUrl = "https://www.autoblog.com/buy/" + str(year) + "-" + make + "-" + \
			model + "/expert-review/"

	#Empty List for review contents
	review = []

	#Add sorceURL for credit
	review.append(baseUrl)
	
	#Iterate through 5 pages of review
	for i in range(1,3):

		#Change url for each page number
		url = baseUrl + "pg-" + str(i) + "/"
		#Fetch Page
		page = requests.get(url)
		#Checks for complete page fetch fail 
		if page.status_code != 200:
			return ("No Reviews Found")

		#Decode with Beautiful Soup
		soup = BeautifulSoup(page.content, 'html.parser')

		#Fetch div id with name "expert-review-content" for summary info
		review_block = soup.find('div', class_="expert-review-content")

		#Grab just text
		text_results = review_block.find_all("p")

		#Check if non review
		if not review_block:
			i = 4
		else:
			review.append(text_results)

	#Return for info
	return (review)
