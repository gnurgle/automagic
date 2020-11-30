import requests
from fuzzywuzzy import fuzz, process
from bs4 import BeautifulSoup

homeLink = 'https://www.rockauto.com'
catalog = '/en/catalog/'


def Car(make, model, year, engine):
    return {
        'Year': year,
        'Make': make,
        'Model': model,
        'Engine':  engine
    }


def get_car_link(car):
    # each car link is a concatenation of homeUrl, catalog, make, model, year, and a unique id
    # this function uses the parameters to find the desired link used to further parse for parts

    # construct our link given parameters
    carUrl = '{0}{1},{2},{3}'.format(homeLink + catalog, car['Make'], car['Year'], car['Model'])
    carPage = requests.get(carUrl)
    soup = BeautifulSoup(carPage.content, 'html.parser')

    # gather the names of engines listed on rockauto
    engineTypes = [label.text for label in soup.find_all('a', class_='navlabellink nvoffset nnormal')[3:]]
    # find closest string match on website with our engine param
    engineMatch = process.extractOne(car['Engine'], engineTypes)[0]
    # Parse rockauto again, this time with our exact match, and we grab the link
    return soup.find('a', class_='navlabellink nvoffset nnormal', text=engineMatch)['href']


def get_car_part_types(year,make,model,engine):
    car = Car(make,model,year,engine)
    engineLink = get_car_link(car)
    # gather the names of parts listed on rockauto
    partsPage = requests.get(homeLink + engineLink)
    soup = BeautifulSoup(partsPage.content, 'html.parser')

    # gather name of listed car parts
    return [label.text for label in soup.find_all('a', class_='navlabellink nvoffset nnormal')][4:]


def get_parts_link(car, part):
    return homeLink + get_car_link(car) + ',' + part.replace(' ', '+').lower()


def get_parts_for_part_type(year,make,model,engine, partType):
    car = Car(make,model,year,engine)
    partsLink = get_parts_link(car, partType)
    partsPage = requests.get(partsLink)

    soup = BeautifulSoup(partsPage.content, 'html.parser')

    tdLabels = soup.find_all('td', class_='nlabel')
    partTypes = [(label.a.text, label.a['href']) for label in tdLabels][5:]

    return tuple(partTypes)

def get_part_listings(partType,partUrl):
	partLink = homeLink + partUrl

	partPage = requests.get(partLink)
	soup = BeautifulSoup(partPage.content, 'html.parser')

	#Get container of parts
	partList = soup.find('div', class_='listing-container-border')
	#Get Listings
	listings = partList.find_all('tbody', class_='listing-inner')

	listingInfo = []
	#Pull Listing info
	for listing in listings:
		#Get Manufacture Name
		manufName = str(listing.find('span', class_='listing-final-manufacturer'))[41:-7]

		#Get Part Number
		partNum = str(listing.find('span', class_='listing-final-partnumber'))[243:-7]
		#Check if PartNum Listing was double digit
		if partNum[2] == '>':
			partNum = partNum[3:]

		#Get Part Name
		partName = str(listing.find('span', class_='span-link-underline-remover'))[42:-7]
		#Check if Part Name has description and remove
		if partName:
			if partName[-1] == '>':
				partName = partName[:-75]

		#Set temp list for links
		linklist = []
		for a in listing.find_all('a', href=True):
			if a.text:
				linklist.append(a['href'])
		#Set part link to first
		partLink = linklist[0]

		#Get Part Description
		partDesc = str(listing.find('div', class_='listing-text-row'))[406:-21]

		#Get Part Price
		partPrice = str(listing.find('span', class_='ra-formatted-amount'))[92:-14]
		#Check if price is out of stock
		if partPrice:
			if partPrice[-1] =='>':
				partPrice = partPrice[29:-7]
			#Check if listing number was double digit
			if partPrice[0] == '>':
				partPrice = partPrice[1:]

		listingInfo.append([manufName,partNum,partName,partDesc,partLink,partPrice])

	return listingInfo

def scrape():
    magicCar = Car('acura', 'tl', 2009, '3.5L V6')

    year = 2009
    make ='acura'
    model='tl'
    engine='3.5L V6'
    
    carPartTypes = get_car_part_types(year,make,model,engine)
    parts = get_parts_for_part_type(year,make,model,engine, carPartTypes[0])

    get_part_listings(magicCar, carPartTypes[0], parts[0])



if __name__ == '__main__':
    scrape()
