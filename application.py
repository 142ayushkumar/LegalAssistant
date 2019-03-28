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
from flask_paginate import Pagination, get_page_args

os.chdir("query3")
from query3.case_names import query_3
os.chdir("..")

os.chdir("Filtering")
# as filter already exists, importing as qfilter
from Filtering.query_filter import filter_query
os.chdir("..")

from date import get_date

# os.chdir("query2")
from query2.act_query import *
from query2.act_query import act_query as query_2
# os.chdir("..")

from query4.fin import *

# os.chdir("query_identifier")
from query_identifier.query_identifier import find_query
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

print("Start")
#load_init()
print("end")

def get_cases(offset=0, per_page=10):
    return books[offset: offset + per_page]


def get_result(query, categories = [], acts = [], judges = [], start_date = None, end_date = None):
    '''
    returns query output as list
    '''
    query_type = find_query(query)
    print(query_type)
    if query_type == 2:
        query_3(query)
        _filePtr = open('query_3.json')
        allResults = json.load(_filePtr)
    elif query_type == 3:
        query_2(query)
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



@app.route("/")
def index():
    print("Here")
    # query = request.args.get('query')
    # categories = request.args.get('category')
    # acts = request.args.get('acts')
    # judges = request.args.get('judge')
    # start_date = request.args.get('from')
    # end_date = request.args.get('to')
    query = categories = acts = judges = start_date = end_date = None
    # if 'query' not in request.form:
    #     return render_template("index.html")
    # if 'query' in request.form:
    #     query = request.form['query']
    # if 'category' in requst.form:
    #     categories = request.form['category']
    # if 'acts' in request.form:
    #     acts = request.form['acts']
    # if 'judge' in request.form:
    #     judges = request.form['judge']
    # if 'from' in request.form:
    #     start_date = request.form['from']
    # if 'to' in request.form:
    #     end_date = request.form['to']


    #Add this search in recents
    store = ""
    temp = query is None and categories is None and acts is None and judges is None and start_date is None and end_date is None
    store = {"query" : query, "categories" : categories, "acts" : acts, "judges" : judges, "start_date" : start_date, "end_date" : end_date}
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
    output = get_result(query=query, categories=categories, acts=acts, judges=judges, start_date=start_date, end_date=end_date)
    # pass the list to be displayed to index.html and render index.html
    return redirect("search.html", output=output)
        

@app.route("/cases/<string:filename>", methods = ['GET'])
def cases(filename):
    print("here")
    print(len(case_data))
    date = case_data[filename][0]
    casename = case_data[filename][1]
    case_id = case_data[filename][2]
    judge = case_data[filename][3]
    verdict = case_data[filename][4]
    act_cited = []
    if filename in acts_cited:
        act_cited = acts_cited[filename]
    category = []
    if filename in categories:
        category = categories[filename]
    citation = []
    if filename in citations:
        citation = citations[filename]
    try:
        file_name = filename + ".txt"
        file = open("OpenSoft-Data/All_FT/" + file_name, 'r')
        content = file.readlines()
    except:
        return render_template('error.html')
    
    return render_template('case.html', case_id=case_id, judge=judge, content=content, casename=casename, verdict=verdict, date=date, acts_cited=act_cited, categories=category, citations=citation)

@app.route("/search", methods=['GET'])
def search():
    query = request.args.get('query')
    categories = request.args.get('category')
    acts = request.args.get('acts')
    judges = request.args.get('judge')
    start_date = request.args.get('from')
    end_date = request.args.get('to')
    print("query is " + query)
    cases_and_acts = query_2(query)
    cases = cases_and_acts["cases"]
    acts = cases_and_acts["acts"]
    print(cases)
    all_cases = list()
    '''
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
                                           
    total = len(query)
    #pagination_cases = get_cases(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    return render_template('search.html',
                           discussions=pagination_discussions,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           username=username
                           )
    '''
    for i,case in enumerate(cases):
        filename = case
        temp = {}
        temp["filename"] = filename
        temp["data"] = case_data[filename][0]
        temp["casename"] = case_data[filename][1]
        temp["case_id"] = case_data[filename][2]
        temp["judge"] = case_data[filename][3]
        temp["verdict"] = case_data[filename][4]
        all_cases.append(temp)
    return render_template('search.html', all_cases=all_cases)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

# @app.errorhandler(500)
# def internal_error(error):
#     return "500 error"


if __name__ == "__main__":
    app.run(host="localhost", port=8080)

