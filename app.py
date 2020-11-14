from flask import Flask, render_template, request, url_for
from forms import *
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    form = CarSelectorForm()    # defined in forms.py

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
        return summary(form.year.data, form.make.data, form.model.data, form.trim.data)

    return render_template('index.html', form=form)


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
    return render_template('summary.html', car=car)


if __name__ == '__main__':
    app.run(debug=True)

