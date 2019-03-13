from flask import Flask, session, render_template, redirect, request
from flask_session import Session

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", method=['POST'])
def index():
    # check if form is submitted
    if 'submit' in request.form:
        #extracting information from forms
        query = request.form['query']
        date = request.form['date']
        category = request.form['category']
        acts = request.form['acts']
        judge = request.form['judge']
        # get results
        output = give_result(query=query, date=date, category=category, acts=acts, judge=judge)
        # pass the list to be displayed to index.html and render index.html
        render_template('index.html', output=output)
    else
        #check ui when there is output and no output, forms should be centered when there is no output
        render_template('index.html')

@app.route("/cases/<string:case_id>", methods = ['GET'])
def cases(case_id):
    render_template('case.html')

