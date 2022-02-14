# This is a sample Python script.

#import all flask modules
from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml

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


# new endpoint to post data
# route decorators - handle both GET (display) and POST (submit)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        symReq = request.form
        psymbol = symReq['symbol']
        return redirect('/symbolsdata?sym=' + psymbol)
    return render_template('index.html')


#new endpoint to fetch and display data
@app.route('/symbolsdata')
def symbolsdata():
    psym = request.args.get('sym')
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM symbols WHERE symbol = '" + psym + "'")
    if resultValue > 0:
        symdataDetails = cur.fetchall()
        return render_template('symboldetails.html', symdataDetails=symdataDetails)


if __name__ == '__main__':
    # debug = True to make sure the changes are reflected immediately
    app.run(debug=True)
