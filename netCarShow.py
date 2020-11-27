import requests
from bs4 import BeautifulSoup
import re

def returnPictureURL(year, make, model):
    baseUrl = "https://www.netcarshow.com/"
    addedUrl = baseUrl + make + '/' + year + '-' + model + '/'
    return addedUrl