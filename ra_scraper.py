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


def get_car_part_types(car):
    engineLink = get_car_link(car)
    # gather the names of parts listed on rockauto
    partsPage = requests.get(homeLink + engineLink)
    soup = BeautifulSoup(partsPage.content, 'html.parser')

    # gather name of listed car parts
    return [label.text for label in soup.find_all('a', class_='navlabellink nvoffset nnormal')][4:]


def get_parts_link(car, part):
    return homeLink + get_car_link(car) + ',' + part.replace(' ', '+').lower()


def get_parts_for_part_type(car, partType):
    partsLink = get_parts_link(car, partType)
    partsPage = requests.get(partsLink)

    soup = BeautifulSoup(partsPage.content, 'html.parser')

    tdLabels = soup.find_all('td', class_='nlabel')
    partTypes = [(label.a.text, label.a['href']) for label in tdLabels][5:]
    return partTypes


def get_part_listings(car, partType, part):
    partLink = homeLink + part[1]   # part is tuple (name, href)
    print(partLink)

    partPage = requests.get(partLink)
    soup = BeautifulSoup(partPage.content, 'html.parser')

    # partList = soup.find_all('table', class_='nobmp')[2:]




def scrape():
    magicCar = Car('acura', 'tl', 2009, '3.5L V6')

    carPartTypes = get_car_part_types(magicCar)

    parts = get_parts_for_part_type(magicCar, carPartTypes[0])

    get_part_listings(magicCar, carPartTypes[0], parts[0])



if __name__ == '__main__':
    scrape()