import sqlite3 as sql
import requests
import json
import copy
from fuzzywuzzy import process

def buildManfId():
	#connect to to DB
	con = sql.connect("base_car.db")
	con.row_factory = sql.Row
	con.text_factory = str
	cur = con.cursor()

	#------Do a create table here -------
	#CREATE TABLE (stuff)
	#------------
	cur.execute("SELECT DISTINCT Make FROM Menu ORDER BY Make")

	rows = cur.fetchall()
	rowTxt = [rows[0][0]]		#RowTxt Contains Make

	for i in range(len(rows)):
		print(rows[i][0])
		rowTxt.append(rows[i][0])
	
	#Pull makes that have passenger cars to narrow down sutible makes
	url = "https://vpic.nhtsa.dot.gov/api/vehicles/GetMakesForVehicleType/car?format=json"
	r = requests.get(url)
	response = json.loads(r.content.decode())
	
	#nhtsaList is the makes from the NHTSA
	nhtsaList = [response['Results'][0]['MakeName']]
	for i in range (1,response['Count'],1):
		nhtsaList.append(response['Results'][i]['MakeName'])
	
	#resMakeID is the MakeID from the NHTSA
	resMakeId = [response['Results'][0]['MakeId']]
	for i in range (1,response['Count'],1):
		resMakeId.append(response['Results'][i]['MakeId'])
	
	
	#Iterate through list of Model+Trim from FuelGov and match to base model NHTSA
	for i in range(len(rowTxt)):
		matchResult = (process.extractOne(nhtsaList[i], rowTxt, score_cutoff = 90))
		if not matchResult:
			print ("No Match found for " + nhtsaList[i])
		else:
			print (matchResult) 
			print ("for " + nhtsaList[i])
			print (matchResult[0])
			for j in range(len(rowTxt)):
				#Syncs up nhtsaList with resMakeID to make sure right ID goes with rowTxt
				if rowTxt[j] == matchResult[0]:
					cur.execute("INSERT OR IGNORE INTO Manf (Make, MakeID) VALUES(?,?)",(rowTxt[j],resMakeId[i]))
					con.commit()
					print (rowTxt[j] + " is ID# " + str(resMakeId[i]))

def buildMakeId():

	#connect to to DB
	con = sql.connect("base_car.db")
	con.row_factory = sql.Row
	con.text_factory = str
	cur = con.cursor()
	
	#Pull Make and MakeId from local database
	cur.execute("SELECT Make,MakeId FROM Manf")
	rows = cur.fetchall()
	
	#rowCheck contains local Make and MakeID(from NHTSA)
	rowCheck = []
	for i in range(len(rows)):
		print(rows[i][0] + str(rows[i][1]))
		rowCheck.append([rows[i][0]])
	for i in range(len(rows)):
		print(rows[i][0] + str(rows[i][1]))
		rowCheck[i].append([rows[i][1]])

	#Iterate over NHTSA DB for each Make to grab avaliable models
	for m in range(len(rows)):
		url = "https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeId/" + str(*rowCheck[m][1]) + "?format=json"
		#URL Verification
		print(url)
		r = requests.get(url)
		response = json.loads(r.content.decode())
		#nhtsaModelList is all models from rowCheck[m][1] make page from NHTSA
		nhtsaModelList = [response['Results'][0]['Model_Name']]
		for i in range (1,response['Count'],1):
			nhtsaModelList.append(response['Results'][i]['Model_Name'])
		
		#resModelId is all model IDs from rowCheck[m][1] make page from NHTSA
		resModelId = [response['Results'][0]['Model_ID']]
		for i in range (1,response['Count'],1):
			resModelId.append(response['Results'][i]['Model_ID'])
	
		#Pulls all unique models from local DB that match rowCheck[m][0] Make
		cur.execute("SELECT DISTINCT Model FROM Menu where Make = ?",(rowCheck[m][0],))

		rows = cur.fetchall()
		
		#rowTxt is all local uniqie model+trim from local DB that match rowCheck[m][0] make
		rowTxt = [rows[0][0]]
		for i in range(len(rows)):
			print(rows[i][0])
			rowTxt.append(rows[i][0])

		#Iterate through each model+trim
		for i in range(len(rowTxt)):
			#Find one that closest matches a base model from NHTSA
			matchResult = (process.extractOne(rowTxt[i], nhtsaModelList, score_cutoff=70))
			if not matchResult:
				print ("No Match found for " + rowTxt[i])
			else:
				#print (matchResult) 
				#print (" for " + rowTxt[i])
				#print (matchResult[0])
				#print (matchResult[0] + " " + rowTxt[i])
				
				#If it's not already a match cut the trim off the model+trim
				if not len(matchResult[0]) == len(rowTxt[i]):
					tempTrim = copy.copy(rowTxt[i])
					modelTrim = tempTrim[len(matchResult[0])+1:]
				else:
					modelTrim = None
				for j in range(len(nhtsaModelList)):
					if nhtsaModelList[j] == matchResult[0]:
						#cur.execute("INSERT OR IGNORE INTO Model (Make, Model, ModelID) VALUES(?,?,?)",(rowCheck[m][0],rowTxt[i],resModelId[j]))
						cur.execute("INSERT OR IGNORE INTO Model (Make, Model, Trim, ModelID) VALUES(?,?,?,?)",(rowCheck[m][0],nhtsaModelList[j],modelTrim,resModelId[j]))
						con.commit()
						#print (rowCheck[m][0] + " " + nhtsaModelList[j] + "is ID# " + str(resModelId[j]) + str(modelTrim))
						print (rowCheck[m][0] + " " + nhtsaModelList[j] + " " + str(modelTrim) + " " + str(resModelId[j]))



def test():
	#connect to to DB
	con = sql.connect("base_car.db")
	con.row_factory = sql.Row
	con.text_factory = str
	cur = con.cursor()

	cur.execute("SELECT Make,MakeId FROM Manf")
	rows = cur.fetchall()
	for i in range(len(rows)):
		print(rows[i][0] + str(rows[i][1]))
	print(rows)
	print("Done")

if __name__ == '__main__':
	buildMakeId()
	#test()
