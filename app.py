from getRecalls import fetchRecalls
from licensePlate import getPlate
from vinDecode import decodeVin
from scrape import singleTrim
from autoblog import fetchReview
from getRecalls import fetchRecalls
from ra_scraper import get_parts_for_part_type, get_part_listings
from flask import Flask, render_template, request, url_for, redirect
from forms import *

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/index', methods=['GET', 'POST'])
def index():

    form = CarSelectorForm()    # defined in forms.py
    plate = StateForm()
    vin = VinForm()

    con = sql.connect('car_base.db')
    con.row_factory = sql.Row
    cur = con.cursor()

    # initialize the drop down menus to a starting value
    # any subsequent changes made to forms are handled by the java script (not here) until submit

    year = form.year.choices[0]
    cur.execute('SELECT DISTINCT Make FROM Base WHERE Year=? ORDER BY Make ASC', [year])
    form.make.choices = [row['Make'] for row in cur.fetchall()]
    make = form.make.choices[0]
    cur.execute('SELECT DISTINCT Model FROM Base WHERE Year=? AND Make=? ORDER BY Model ASC', (year, make))
    form.model.choices = [row['Model'] for row in cur.fetchall()]
    model = form.model.choices[0]
    cur.execute('SELECT Trim FROM Base WHERE Year=? AND Make=? AND Model=? ORDER BY Trim ASC', (year, make, model))
    form.trim.choices = [row['Trim'] for row in cur.fetchall()]

    if request.method == 'POST':
        url = "/" + str(form.year.data) + "/" + form.make.data + "/" + form.model.data + "/" + form.trim.data + "/summary"
        return redirect(url)
		#return redirect(url_for('summary(form.year.data, form.make.data, form.model.data, form.trim.data)'))

    return render_template('index.html', form=form, plate=plate, vin=vin)


# drop down handling when year, make, or model changes
@app.route('/<year>/<make>/<model>/trim')
def trim(year, make, model):
    con = sql.connect('car_base.db')
    con.row_factory = sql.Row
    cur = con.cursor()

    cur.execute('SELECT Trim FROM Base WHERE Year=? AND Make=? AND Model=?', (year, make, model))
    return {'trims': [row['Trim'] for row in cur.fetchall()]}


# drop down handling when year or make changes
@app.route('/<year>/<make>/model/trim')
def modelTrim(year, make):
    con = sql.connect('car_base.db')
    con.row_factory = sql.Row
    cur = con.cursor()

    cur.execute('SELECT DISTINCT Model FROM Base WHERE Year=? AND Make=?', (year, make))
    result = {'models': [row['Model'] for row in cur.fetchall()]}
    result.update(trim(year, make, result['models'][0]))
    return result


# drop down handling when year changes
@app.route('/<year>/make/model/trim')
def makeModelTrim(year):
    con = sql.connect('car_base.db')
    con.row_factory = sql.Row
    cur = con.cursor()

    cur.execute('SELECT DISTINCT Make FROM Base WHERE Year=? ORDER BY Year ASC', [year])

    result = {}
    result['makes'] = [row['Make'] for row in cur.fetchall()]
    result.update(modelTrim(year, result['makes'][0]))
    return result


# endpoint for a distinct vehichle
@app.route('/<year>/<make>/<model>/<trim>/summary')
def summary(year, make, model, trim):
    car = {
        'Year': year,
        'Make': make,
        'Model': model,
        'Trim': trim
    }
    return summaryPage(year,make,model,trim)
    #return render_template('summary.html', car=car)

#wrapper for YMMT form
@app.route('/YMMT', methods=['POST'])
def ymmt():

	form = CarSelectorForm()
	plate = StateForm()
	vin = VinForm()

	if request.method == 'POST':
		url = "/" + str(form.year.data) + "/" + form.make.data + "/" + form.model.data + "/" + form.trim.data + "/summary"
		return redirect(url)

	return render_template('index.html', form=form, plate=plate, vin=vin)

#wrapper for Plate form
@app.route('/plate', methods=['POST'])
def plate():

	form = CarSelectorForm()
	plate = StateForm()
	vin = VinForm()

	if request.method == 'POST':
		outputVIN = getPlate(plate.state.data,plate.plate.data) 
		if outputVIN == "ER-NoPlate":
			return render_template('index.html', form=form, plate=plate, vin=vin)
		return vinPass(outputVIN)
	return render_template('index.html', form=form, plate=plate, vin=vin)

#wrapper for VIN form
@app.route('/vin', methods=['POST'])
def vinParse():

	form = CarSelectorForm()
	plate = StateForm()
	vin = VinForm()

	if request.method == 'POST':
		outputYMMT = decodeVin(vin.number.data) 
		if outputYMMT[0] == "ER-BadVin":
			return render_template('index.html', form=form, plate=plate, vin=vin)
		url = "/" + str(outputYMMT[0]) + "/" + outputYMMT[1] + "/" + outputYMMT[2] + "/" + outputYMMT[3] + "/summary"
		return redirect(url)

	return render_template('index.html', form=form, plate=plate)

#Handler for passed Vin value
def vinPass(vinput):
	form = CarSelectorForm()
	plate = StateForm()
	vin = VinForm()

	outputYMMT = decodeVin(vinput) 

	if outputYMMT[0] == "ER-BadVin":
		return render_template('index.html', form=form, plate=plate, vin=vin)

	url = "/" + str(outputYMMT[0]) + "/" + outputYMMT[1] + "/" + outputYMMT[2] + "/" + outputYMMT[3] + "/summary"
	return redirect(url)

#Display summary of vehicle information
@app.route('/summary')
def summaryPage(year, make, model, trim):

	#Open DB
	conn = sql.connect('car_base.db')
	cur = conn.cursor()

	#Pull Data
	cur.execute("SELECT * FROM Base WHERE Year = ? AND Make = ? AND Model = ? \
		AND Trim = ?",(year,make,model,trim))

	#Grab results
	results = cur.fetchall()

	#Check if results are empty
	if not results:
		#Run scraper to check for potential missed trim
		singleTrim(year,make,model,trim)

		#Rerun SQL query
		cur.execute("SELECT * FROM Base WHERE Year = ? AND Make = ? AND Model = ? \
			AND Trim = ?",(year,make,model,trim))

		#Grab results
		results = cur.fetchall()

	#Check for empty results again
	if not results:
		#If empty again, dump to index
		#This state should never be reached, all data is using the same DB
		print("Error reading "+str(year)+" "+make+" "+model+" "+trim)
		return home()

		
	cur.close()
	conn.close()
	return render_template('summary.html', results=results[0])

#Display Car review
@app.route('/<year>/<make>/<model>/<trim>/review')
def getReview(year,make,model,trim):
	results = [year,make,model,trim]
	return render_template('review.html', results=results, review=fetchReview(year,make,model))

#Display Car Recalls
@app.route('/<year>/<make>/<model>/<trim>/recalls')
def recalls(year,make,model,trim):
	results = [year,make,model,trim]
	return render_template('recalls.html', results=results, recalls=fetchRecalls(year,make,model))

#Display Parts
@app.route('/<year>/<make>/<model>/<trim>/parts')
def parts(year,make,model,trim):

	#connect to Database
	conn = sql.connect('car_base.db')
	cur = conn.cursor()

	#Select Engine
	cur.execute("SELECT Engine FROM Base WHERE Year=? AND Make=? AND Model=? \
		AND Trim=?",(year,make,model,trim))

	#Fetch engine value
	engineRes = cur.fetchone()

	#Strip tuple out
	engine = engineRes[0]

	#Pass basic info
	results = [year,make,model,trim]

	#Create form
	partForm = PartForm()
	#Update Drop down Choices
	partForm.partCat.choices=partForm.getParts(year,make,model,engine)

	#Render page
	return render_template('parts.html', part=partForm, results=results)

#Route for part listing
@app.route('/<year>/<make>/<model>/<trim>/<partCat>/partList')
def getPartList(year,make,model,trim,partCat):

	#connect to Database
	conn = sql.connect('car_base.db')
	cur = conn.cursor()

	#Select Engine
	cur.execute("SELECT Engine FROM Base WHERE Year=? AND Make=? AND Model=? \
		AND Trim=?",(year,make,model,trim))

	#Fetch engine value
	engineRes = cur.fetchone()

	#Strip tuple out
	engine = engineRes[0]

	#Get part list
	parts = get_parts_for_part_type(year,make,model,engine,partCat)

	#Strip name from returned list
	result = []
	for part in parts:
	#	result.append(part[0])
		result.append(part[0])
	#resultDict = {result[i]: result[i+1] for i in range(0,len(result),2)} 
	#print (resultDict)
	#Return list of names
	return {'partList': [results for results in result]}
	#return {'partList': resultDict}
#Display Listings
@app.route('/<year>/<make>/<model>/<trim>/partListings', methods=['POST'])
def listParts(year,make,model,trim):

	part = PartForm()

	if request.method == 'POST':

		#connect to Database
		conn = sql.connect('car_base.db')
		cur = conn.cursor()

		#Select Engine
		cur.execute("SELECT Engine FROM Base WHERE Year=? AND Make=? AND Model=? \
			AND Trim=?",(year,make,model,trim))

		#Fetch engine value
		engineRes = cur.fetchone()

		#Strip tuple out
		engine = engineRes[0]

		#Get URL for part
		parts = get_parts_for_part_type(year,make,model,engine,part.partCat.data)
		check = str(part.partList.data)

		partUrl = ""
		for partu in parts:
			if partu[0] == check:
				partUrl = partu[1]

		print (partUrl)
		listing = get_part_listings(part.partCat.data,partUrl)
		print (listing)

		results = [year,make,model,trim]
		title=[part.partCat.data,part.partList.data]

		return render_template('listings.html', results=results, listings=listing, title=title)
	return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)

