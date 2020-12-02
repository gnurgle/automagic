import sqlite3 as sql
import requests
import json
import copy
from scrape import singleScrape
from fuzzywuzzy import process


def newDBEntries():
    # connect to to DB
    con = sql.connect("car_base.db")
    con.row_factory = sql.Row
    con.text_factory = str
    cur = con.cursor()

    cur.execute("SELECT Make, Model, Year FROM Base")
    rows = cur.fetchall()

    makeCheck = []
    modelCheck = []
    yearCheck = []
    for i in range(len(rows)):
        makeCheck.append([rows[i][0]])
    for i in range(len(rows)):
        modelCheck.append([rows[i][1]])
    for i in range(len(rows)):
        yearCheck.append([rows[i][2]])


    # Pull car makes
    url = "https://vpic.nhtsa.dot.gov/api/vehicles/GetMakesForVehicleType/truck?format=json"
    # URL Verification
    print(url)
    r = requests.get(url)
    response = json.loads(r.content.decode())

    # makeList is the makes from the NHTSA
    makeList = [response['Results'][0]['MakeName']]
    for i in range(1, response['Count'], 1):
        makeList.append(response['Results'][i]['MakeName'])

    # makeID is the MakeID from the NHTSA
    makeId = [response['Results'][0]['MakeId']]
    for i in range(1, response['Count'], 1):
        makeId.append(response['Results'][i]['MakeId'])


    for m in range(len(makeList)):
        url = "https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeId/" + str(*makeId[m]) + "?format=json"
        # URL Verification
        print(url)
        r = requests.get(url)
        response = json.loads(r.content.decode())

        modelList = [response['Results'][0]['Model_Name']]
        for i in range(1, response['Count'], 1):
            modelList.append(response['Results'][i]['Model_Name']


        for k in range(len(modelList)):
            for j in range(1981,2021):
                for g in range(len(makeCheck)):
                    matchResult = (process.extractOne(makeCheck[g], makeList, score_cutoff=70)
                    if not matchResult:
                        print("No Match found for " + makeCheck[g])
                    else:
                        for p in range(len(makeList)):
                            makeList[p].lower()
                            makeList[p].capitalize()
                            if makeList[p] == matchResult[0]:
                                singleScrape(j, makeList[m], modelList[k])



if __name__ == '__main__':
    newDBEntries()
