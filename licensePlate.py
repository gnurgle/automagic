#This file takes in a state and plate and outputs a VIN number associated with
#the vehicle the plate is registered to
import requests
import json

def getPlate(state,plate):

	#Use url found through network packet sniffing
	#This URL is the pass through form entering in the license information
	#to passing it internally and rendering the page with just the vin number
	#by intercepting the passing url we can extract just the vin number
	#to be used in a normal vin identification
	
	url = "https://www.vehiclehistory.com/graphql?operationName=" + \
		"licensePlate&variables=%7B%22number%22%3A%22" + \
		plate + " %22%2C%22state%22%3A%22" + state + \
		"%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22" + \
		"version%22%3A1%2C%22sha256Hash%22%3A%22fefee74e293c6b0" + \
		"ece44ebed7d3e25bf70102209c21f773b80b31abb108ece75%22%7D%7D"

	#Get content of json 
	response = requests.get(url).text
	r = json.loads(response)

	#Failsafe in case of vin not present

	if not r['data']['licensePlate']['vin']:
		return("ER-NoPlate")
	else:
		#Return Vin
		return(r['data']['licensePlate']['vin'])

#if __name__=="__main__":
#	getPlate("FL","ITSDAD")
