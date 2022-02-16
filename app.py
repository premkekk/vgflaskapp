# This is a sample Python script.

#import all flask modules
from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml
import pandas as pd

#instantiate flask object
app = Flask(__name__)

# Configure db using yaml
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

# instantiate mysql object
mysql = MySQL(app)


# new endpoint to post data using textbox as input
# route decorators - handle both GET (display) and POST (submit)
@app.route('/textbox', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        symReq = request.form
        psymbol = symReq['symbol']
        return redirect('/symbolhist?sym=' + psymbol)
    return render_template('textbox.html')


# new endpoint to post data using dropdown as input
# route decorators - handle both GET (display) and POST (submit)
@app.route('/', methods=['GET', 'POST'])
def dropdown():
    if request.method == 'POST':
        symReq = request.form
        psymbol = symReq['ddSymbols']
        return redirect('/linechart?sym=' + psymbol)
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT DISTINCT SYMBOL FROM symbols ORDER BY 1")
    if resultValue > 0:
        symdataDetails = cur.fetchall()
        return render_template('dropdown.html', symdataDetails=symdataDetails)


#new endpoint to fetch and display symbolsinfo
@app.route('/symbolsinfo')
def symbolsdata():
    psym = request.args.get('sym')
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM symbols WHERE symbol = '" + psym + "'")
    if resultValue > 0:
        symdataDetails = cur.fetchall()
        return render_template('symbolinfo.html', symdataDetails=symdataDetails)


#new endpoint to fetch and display historical symbol data
@app.route('/symbolhist')
def symbolhist():
    psym = request.args.get('sym')
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT SYMBOL, HISTDATE, OPENPRICE, CLOSEPRICE, HIGHPRICE, LOWPRICE FROM symhistory WHERE symbol = '" + psym + "' and histdate > '2022-01-01'")
    if resultValue > 0:
        symdataDetails = cur.fetchall()
        return render_template('symbolhist.html', symdataDetails=symdataDetails)


#new endpoint to fetch and display historical symbol data
@app.route('/linechart')
def linechart():
    psym = request.args.get('sym')
    cur = mysql.connection.cursor()
    resultValue = cur.execute(" SELECT SYMBOL, DATE_FORMAT(HISTDATE, '%Y-%m-%d') as HISTDATE, ROUND(OPENPRICE,2) as OPENPRICE, ROUND(CLOSEPRICE,2) as CLOSEPRICE, " +
                              " ROUND(HIGHPRICE,2) as HIGHPRICE, ROUND(LOWPRICE,2) AS LOWPRICE, VOLUME " +
                              " FROM symhistory " +
                              " WHERE symbol = '" + psym + "' and histdate > '2022-01-01'")
    if resultValue > 0:
        symdataDetails = cur.fetchall()
        lstDt = pd.DataFrame(list(symdataDetails))[1].to_list()
        lstOP = pd.DataFrame(list(symdataDetails))[2].to_list()
        lstCP = pd.DataFrame(list(symdataDetails))[3].to_list()
        lstHP = pd.DataFrame(list(symdataDetails))[4].to_list()
        lstLP = pd.DataFrame(list(symdataDetails))[5].to_list()
        return render_template('linechart.html', symbol=psym, labels=lstDt, openprice=lstOP, closeprice=lstCP, highprice=lstHP, lowprice=lstLP)


if __name__ == '__main__':
    # debug = True to make sure the changes are reflected immediately
    app.run(debug=True)
