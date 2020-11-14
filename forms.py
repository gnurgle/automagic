from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, validators
import sqlite3 as sql


class CarSelectorForm(FlaskForm):
    con = sql.connect('car_base.db')
    con.row_factory = sql.Row
    cur = con.cursor()

    cur.execute('SELECT DISTINCT Year FROM Base WHERE Year!=? ORDER BY Year DESC', ['Not on File'])
    yearList = [row['Year'] for row in cur.fetchall()]

    year = SelectField('year', choices=yearList)
    # We always have the year box loaded to begin with, rest is handled in /index
    make = SelectField('make', choices=[])
    model = SelectField('model', choices=[])
    trim = SelectField('trim', choices=[])

class VinForm(FlaskForm):
	number = StringField('Number', [validators.InputRequired()])

class StateForm(FlaskForm):
	state = SelectField('state', choices=[("AL","Alabama"),\
	("AK", "Alaska"),\
	("AZ", "Arizona"),\
	("AR", "Arkansas"),\
	("CA", "California"),\
	("CO", "Colorado"),\
	("CT", "Connecticut"),\
	("DE", "Delaware"),\
	("DC", "District of Columbia"),\
	("FL", "Florida"),\
	("GA", "Georgia"),\
	("HA", "Hawaii"),\
	("ID", "Idaho"),\
	("IL", "Illinois"),\
	("IN", "Indiana"),\
	("IA", "Iowa"),\
	("KS", "Kansas"),\
	("KY", "Kentucky"),\
	("LA", "Louisiana"),\
	("ME", "Maine"),\
	("MD", "Maryland"),\
	("MA", "Massachusetts"),\
	("MI", "Michigan"),\
	("MN", "Minnesota"),\
	("MS", "Mississippi"),\
	("MO", "Missouri"),\
	("MT", "Montana"),\
	("NE", "Nebraska"),\
	("NV", "Nevada"),\
	("NH", "New Hampshire"),\
	("NJ", "New Jersey"),\
	("NM", "New Mexico"),\
	("NY", "New York"),\
	("NC", "North Carolina"),\
	("ND", "North Dakota"),\
	("OH", "Ohio"),\
	("OK", "Oklahoma"),\
	("OR", "Oregon"),\
	("PN", "Pennsylvania"),\
	("RI", "Rhode Island"),\
	("SC", "South Carolina"),\
	("SD", "South Dakota"),\
	("TN", "Tennessee"),\
	("TX", "Texas"),\
	("UT", "Utah"),\
	("VT", "Vermont"),\
	("VA", "Virginia"),\
	("WA", "Washington"),\
	("WV", "West Virginia"),\
	("WI", "Wisconsin"),\
	("WY", "Wyoming")])
	plate = StringField('New Value', [validators.InputRequired()])
