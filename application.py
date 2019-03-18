from flask import Flask, session, render_template, redirect, request
from flask_session import Session

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_result(query, category, acts, judge, start_date, end_date):
    return 1

@app.route("/", methods = ['GET', 'POST'])
def index():
    # check if form is submitted
    data = request.method
    print(data)
    if 'search' in request.form:
        print("here")
        #extracting information from forms
        query = request.form['query']
        category = request.form['category']
        acts = request.form['acts']
        judge = request.form['judge']
        start_date = request.form['from']
        end_date = request.form['to']
        print(f"query is {query}, category is {category}, acts is {acts}, judge is {judge}, start date is {start_date}")
        # get results
        output = get_result(query=query, category=category, acts=acts, judge=judge, start_date=start_date, end_date=end_date)
        # pass the list to be displayed to index.html and render index.html
        return render_template('index.html', output=output)
    else :
        #check ui when there is output and no output, forms should be centered when there is no output
        return render_template('index.html')

@app.route("/cases/<string:case_id>", methods = ['GET', 'POST'])
def cases(case_id):
    return render_template('case.html', case_id )

