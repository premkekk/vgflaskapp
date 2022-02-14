# This is a sample Python script.

#import all flask modules
from flask import Flask, render_template

#instantiate flask object
app = Flask(__name__)

#new endpoint to fetch and display historical symbol data
@app.route('/')
def linechart():
    #psym = request.args.get('sym')
    data = [
        ("2022-01-01", 300),
        ("2022-01-02", 301),
        ("2022-01-03", 302),
        ("2022-01-04", 303),
        ("2022-01-05", 304),
    ]
    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    return render_template('linechart.html', labels=labels, values=values)


if __name__ == '__main__':
    # debug = True to make sure the changes are reflected immediately
    app.run(debug=True)
