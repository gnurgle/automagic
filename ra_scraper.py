import requests
from fuzzywuzzy import fuzz, process
from bs4 import BeautifulSoup

homeLink = 'https://www.rockauto.com'
catalog = '/en/catalog/'


def get_car_link( make, year, model, engine):
    # each car link is a concatenation of homeUrl, catalog, make, model, year, and a unique id
    # this function uses the parameters to find the desired link used to further parse for parts

    # construct our link given parameters
    carUrl = '{0}{1},{2},{3}'.format(homeLink + catalog, make, year, model)
    carPage = requests.get(carUrl)

    soup = BeautifulSoup(carPage.content, 'html.parser')

    # gather the names of engines listed on rockauto
    engineTypes = [label.text for label in soup.find_all('a', class_='navlabellink nvoffset nnormal')[3:]]

    # find closest string match on website with our engine param
    engineMatch = process.extractOne(engine, engineTypes)[0]

    # Parse rockauto again, this time with our exact match, and we grab the link
    return soup.find('a', class_='navlabellink nvoffset nnormal', text=engineMatch)['href']


def get_car_part_types(make, year, model, engine):

    engineLink = get_car_link(make, year, model, engine)
    # gather the names of parts listed on rockauto
    partsPage = requests.get(homeLink + engineLink)
    soup = BeautifulSoup(partsPage.content, 'html.parser')

    # gather name of listed car parts
    return [label.text for label in soup.find_all('a', class_='navlabellink nvoffset nnormal')][4:]


def get_parts_for_part_type(make, year, model, engine, part):

    engineLink = get_car_link(make, year, model, engine)
    part = part.replace(' ', '+').lower()
    partsLink = homeLink + engineLink + ',' + part

    partPage = requests.get(partsLink)

    soup = BeautifulSoup(partPage.content, 'html.parser')

    tdLabels = soup.find_all('td', class_='nlabel')
    partTypes = [label.a.text for label in tdLabels][5:]
    return partTypes


def scrape():
    carPartTypes = get_car_part_types('acura', 2008, 'tl', '3.2L V6 SOHC 24V')
    parts = get_parts_for_part_type('acura', 2008, 'tl', '3.2L V6 SOHC 24V', carPartTypes[0])
    print(parts)


if __name__ == '__main__':
    scrape()