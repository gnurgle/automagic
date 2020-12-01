import sqlite3 as sql
import requests
import json
import copy
import scrape.py
from fuzzywuzzy import process


def buildManfId():
    # connect to to DB
    con = sql.connect("base_car.db")
    con.row_factory = sql.Row
    con.text_factory = str
    cur = con.cursor()

    cur.execute("SELECT DISTINCT Make FROM Menu ORDER BY Make")

    rows = cur.fetchall()
    rowTxt = [rows[0][0]]  # RowTxt Contains Make

    for i in range(len(rows)):
        print(rows[i][0])
        rowTxt.append(rows[i][0])

    # Pull makes that have passenger cars to narrow down sutible makes
    url = "https://vpic.nhtsa.dot.gov/api/vehicles/GetMakesForVehicleType/car?format=json"
    r = requests.get(url)
    response = json.loads(r.content.decode())

    # nhtsaList is the makes from the NHTSA
    nhtsaList = [response['Results'][0]['MakeName']]
    for i in range(1, response['Count'], 1):
        nhtsaList.append(response['Results'][i]['MakeName'])

    # resYear is the year from the NHTSA
    resYear = [response['Results'][0]['Year']]
    for i in range(1, response['Count'], 1):
        resYear.append(response['Results'][i]['Year'])

    # Iterate through list of Model+Year from FuelGov and match to base model NHTSA
    for i in range(len(rowTxt)):
        matchResult = (process.extractOne(nhtsaList[i], rowTxt, score_cutoff=90))
        if not matchResult:
            print("No Match found for " + nhtsaList[i])
        else:
            print(matchResult)
            print("for " + nhtsaList[i])
            print(matchResult[0])
            for j in range(len(rowTxt)):
                # Syncs up nhtsaList with resYear to make sure right ID goes with rowTxt
                if rowTxt[j] == matchResult[0]:
                    cur.execute("INSERT OR IGNORE INTO Manf (Make, Year) VALUES(?,?)", (rowTxt[j], resYear[i]))
                    con.commit()
                    print(rowTxt[j] + " is Year " + str(resYear[i]))


def newDBEntries():
    # connect to to DB
    con = sql.connect("base_car.db")
    con.row_factory = sql.Row
    con.text_factory = str
    cur = con.cursor()

    # Pull Make and year from local database
    cur.execute("SELECT Make,Year FROM Manf")
    rows = cur.fetchall()

    # rowCheck contains local Make and year(from NHTSA)
    rowCheck = []
    for i in range(len(rows)):
        print(rows[i][0] + str(rows[i][1]))
        rowCheck.append([rows[i][0]])
    for i in range(len(rows)):
        print(rows[i][0] + str(rows[i][1]))
        rowCheck[i].append([rows[i][1]])

    # Iterate over NHTSA DB for each Make to grab avaliable models
    for m in range(len(rows)):
        url = "https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeId/" + str(*rowCheck[m][1]) + "?format=json"
        # URL Verification
        print(url)
        r = requests.get(url)
        response = json.loads(r.content.decode())
        # nhtsaModelList is all models from rowCheck[m][1] make page from NHTSA
        nhtsaModelList = [response['Results'][0]['Model_Name']]
        for i in range(1, response['Count'], 1):
            nhtsaModelList.append(response['Results'][i]['Model_Name'])

        # resModelId is all years from rowCheck[m][1] make page from NHTSA
        resYear = [response['Results'][0]['Year']]
        for i in range(1, response['Count'], 1):
            resYear.append(response['Results'][i]['Year'])

        # Pulls all unique models from local DB that match rowCheck[m][0] Make
        cur.execute("SELECT DISTINCT Model FROM Menu where Make = ?", (rowCheck[m][0],))

        rows = cur.fetchall()

        # rowTxt is all local uniqie model+trim from local DB that match rowCheck[m][0] make
        rowTxt = [rows[0][0]]
        for i in range(len(rows)):
            print(rows[i][0])
            rowTxt.append(rows[i][0])



        # select values from NHTSA that are not in the car_base.db
        cur.execute("SELECT DISTINCT Year,Make, Model FROM Model EXCEPT SELECT Year,Make,Model FROM Base")

        rows = cur.fetchall()
        rowTxt = []

        # rowTxt contains Year,Make, Model to be passed into scrape.py
        for i in range(len(rows)):
            print(rows[i][0] + str(rows[i][1]))
            rowTxt[i].append([rows[i][0]])
        for i in range(len(rows)):
            print(rows[i][0] + str(rows[i][1]))
            rowTxt[i].append([rows[i][1]])
        for i in range(len(rows)):
            print(rows[i][0] + str(rows[i][2]))
            rowTxt[i].append([rows[i][2]])


        for i in range(len(rowTxt)):
            # Find one that closest matches a base model from NHTSA
            matchResult = (process.extractOne(rowTxt[i], resYear[i] + rowCheck[i][0] + nhtsaModelList[i], score_cutoff=80))
            if not matchResult:
                print("No Match found for " + rowTxt[i])
            else:
                sortArgs("-s",rows[i][0],rows[i][1],rows[i][2])


if __name__ == '__main__':
    newDBEntries()
