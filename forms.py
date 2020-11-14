from flask_wtf import FlaskForm
from wtforms import SelectField
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
