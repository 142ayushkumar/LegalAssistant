from flask import Flask, session, render_template, redirect, request, make_response 
from flask_session import Session
from collections import defaultdict
import os
import json
import datetime
import operator
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
stop_words = set(stopwords.words('english'))
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

os.chdir("query3")
from query3.case_names import query_3
os.chdir("..")

os.chdir("Filtering")
# as filter already exists, importing as qfilter
from Filtering.query_filter import filter_query
os.chdir("..")

from date import get_date

# os.chdir("query2")
from query2.query2 import query2 as query_2
# os.chdir("..")

# os.chdir("query_identifier")
# from query_identifier.query_identifier import find_query
# os.chdir("..")


app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

case_data_file = open("./data/file_to_date_casename_casecode_judge_judgment.json")
case_data = json.load(case_data_file)

acts_cited_file = open("./data/case_to_acts.json")
acts_cited = json.load(acts_cited_file)

categories_file = open("./data/case_to_subjects.json")
categories = json.load(categories_file)

citations_file = open("./data/case_citations_name.txt")
citations = json.load(citations_file)

def get_result(query, categories = [], acts = [], judges = [], start_date = None, end_date = None):
    '''
    returns query output as list
    '''
    query_type = find_query(query)

    if query_type == 2:
        query_3(query)
        _filePtr = open('query_3.json')
        allResults = json.load(_filePtr)
    elif query_type == 3:
        query2(query)
        _filePtr = open('query2.json')
        allResults = json.load(_filePtr)
    else:
        print(1, 4)
        #query other than 2 and 3

    print(allResults["acts"])
    print(allResults["cases"])
    
    allResultsList = []
    for case in allResults["cases"]:
        allResultsList.append(case)

    queryToPerform = {}
    queryToPerform["categories"] = categories
    queryToPerform["acts"] = acts
    queryToPerform["judges"] = judges

    filterResult = {}

    filterResult = query_filter(allResultsList, queryToPerform)

    prefinalResult = []

    if start_date != None and end_date != None:
        _startdate = get_date(start_date)
        _enddate = get_date(end_date)

        for case in filterResult:
            current_date = get_date(filterResult[case]["date"])
            if _startdate <= current_date <= _enddate:
                prefinalResult.append((allResults[case[0]], case[0]))
    else :
        for case in filterResult:
            prefinalResult.append((allResults[case[0]], case[0]))

    prefinalResult.sort(reverse = True)

    finalList = []
    for case in prefinalResult:
        finalList.append(case[1]) 

    return finalList



@app.route("/", methods = ['GET'])
def index():
    query = request.args.get('query')
    category = request.args.get('category')
    acts = request.args.get('acts')
    judge = request.args.get('judge')
    start_date = request.args.get('from')
    end_date = request.args.get('to')
    #Add this search in recents
    store = ""
    temp = query is None and category is None and acts is None and judge is None and start_date is None and end_date is None
    store = {"query" : query, "category" : category, "acts" : acts, "judge" : judge, "start_date" : start_date, "end_date" : end_date}
    if temp:
        if 'recent' not in session:
            session["recent"] = []
        recents = session["recent"]
        return render_template('index.html', recents=recents)
    if len(session["recent"]) >= 5:
        print("here")
        session["recent"] = session["recent"][0:5]
    session["recent"] = [store] + session["recent"]
    # get results
    output = get_result(query=query, categories=category, acts=acts, judge=judge, start_date=start_date, end_date=end_date)
    # pass the list to be displayed to index.html and render index.html
    return render_template('search.html', output=output)
        

@app.route("/cases/<string:filename>", methods = ['GET'])
def cases(filename):
    date = case_data[filename][0]
    casename = case_data[filename][1]
    case_id = case_data[filename][2]
    judge = case_data[filename][3]
    verdict = case_data[filename][4]
    try:
        file_name = filename + ".txt"
        file = open("OpenSoft-Data/All_FT/" + file_name, 'r')
        content = file.readlines()
    except:
        return render_template('error.html')
    return render_template('case.html', case_id=case_id, judge=judge, content=content, casename=casename, verdict=verdict, date=date, acts_cited=acts_cited[filename], categories=categories[filename], citations=citations[filename])

@app.route("/search", methods=['GET'])
def search():
    return render_template('search.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)

