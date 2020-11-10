import copy
import requests
from flask import Flask, render_template, request
import sqlite3 as sql
from bs4 import BeautifulSoup
app = Flask(__name__)

def getCar(yr, mke, mdl,trm):
    year = yr
    make = mke
    model = mdl
    trim = trm
    zipCode = 32168
    resultURl = 'https://www.autotrader.com/cars-for-sale/all-cars/'
    makeURL = resultURl + str(year) + '/' + str(make) + '/' + str(model) + '/' + str(zipCode) + '?searchRadius=0&trimCode=' + '%7C' + str(trim)
    print (makeURL)
    return makeURL

if __name__ == '__main__': #main method
    yr = input("Year ")
    mke = input("Make ")
    mdl = input("Model ")
    trm = input("Trim ")
    getCar(yr,mke,mdl,trm)
