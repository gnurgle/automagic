import requests
from bs4 import BeautifulSoup
import re

def returnPictureURL(year, make, model):
    baseUrl = "https://www.netcarshow.com/"
    addedUrl = baseUrl + make + '/' + year + '-' + model + '/' + "1280x960/wallpaper_01.htm"
    return addedUrl