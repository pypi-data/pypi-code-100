import os
import psycopg2
import heroku3
import subprocess
import json
from flask import Flask, request, render_template, Response
from .debugger import stresstest

API_KEY = '2aaf98e1-4dd6-4353-a88c-0051be97821a' 
app = Flask(__name__)


# Index route
@app.route('/')
def home():
    return render_template("index.html")


# Scripts route
@app.route('/scripts')
def scripts():
    return render_template("scripts.js")


# Show Submissions route
@app.route('/showSub')
def showSub():
    return render_template("showSub.html")


# Show 10 rows from the database
@app.route('/showRows', methods=["POST"])
def showRows():
    page = int(request.form['page'])
    # using heroku API-KEY to obtain current database_url
    app = heroku3.from_key(API_KEY).app('multiprocessing-stress-tester')
    DATABASE_URL = app.config()['DATABASE_URL']

    # connecting to the database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # executing select to have rows for the table
    cur.execute("SELECT * FROM submission ORDER BY test_id DESC;")
    all_rows = cur.fetchall()
    index_row = (page - 1) * 10
    if (index_row >= len(all_rows)):
        index_row, page = 0, 1
    curr_rows = all_rows[index_row : min(index_row+10, len(all_rows))]

    # setting response's output
    resp = Response(json.dumps({'page': page, 'rows': curr_rows}))
    resp.mimetype = "application/json"
    
    return resp


# Reading 4 files (generator, checker, correct, wrong) which contain respectively:
# generator: a .cpp file containing a generator of a test case
# checker: a .cpp file containing a checker in order to see
#          if the wrong solution has the same result of the correct one
# correct: a .cpp file containing a solution that should be correct
#          for every test case
# wrong: a .cpp file containing a possible solution (we don't know whether
#        it works for every test case or not)
#
# The method returns the test_id of the stress-test in the database
# and the debugger result obtained by these files.
@app.route('/sub', methods=["POST"])
def exec_sub():
    # reading input and formatting in order to 
    # execute the submit method
    cpp_files = [request.files['generator'].read().decode('utf-8'),
                 request.files['checker'].read().decode('utf-8'),
                 request.files['correct'].read().decode('utf-8'),
                 request.files['wrong'].read().decode('utf-8')]
    safety = request.form['safety'] == "True"
    testcase = int(request.form['testcase'])
    timelimit = float(request.form['timelimit'])

    # executing the stresstest and the submit
    test_id, dbg_res = submit(cpp_files, safety, testcase, timelimit)

    # setting response's output
    resp = Response(json.dumps({'id' : test_id,
                                'result' : dbg_res}))
    resp.mimetype = "application/json"
    return resp


# Executes the stresstest and submit the result in the database
# cpp_files[0]: string
#               generator.cpp string
# cpp_files[1]: string
#               checker.cpp string
# cpp_files[2]: string
#               correct.cpp string
# cpp_files[3]: string
#               wrong.cpp string
# safety: bool
#       safety's stresstest boolean value
# testcase: int
#           number of testcases to perform in the stresstest
# timelimit: float
#           timelimit of wrong.cpp execution in seconds
def submit(cpp_files, safety, testcase, timelimit):
    # using heroku API-KEY to obtain current database_url
    app = heroku3.from_key(API_KEY).app('multiprocessing-stress-tester')
    DATABASE_URL = app.config()['DATABASE_URL']

    # connecting to the database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # executing a temporary insert to have the submission id
    cur.execute("INSERT INTO submission (generator," +
                "checker, correct, wrong, result) VALUES ('" +
                cpp_files[0].replace("'", "''") + "', '" +
                cpp_files[1].replace("'", "''") + "', '" +
                cpp_files[2].replace("'", "''") + "', '" +
                cpp_files[3].replace("'", "''") + "', -1) RETURNING test_id;")
    test_id = cur.fetchone()[0]

    # creating temporary files and testing directory
    subprocess.call(['mkdir', f'id_{test_id}/'])
    os.chdir(f'id_{test_id}/')
    with open('generator.cpp', 'w', encoding='utf-8') as out_gen:
        subprocess.run(['echo', cpp_files[0]], stdout=out_gen, check=False)
    with open('checker.cpp', 'w', encoding='utf-8') as out_check:
        subprocess.run(['echo', cpp_files[1]], stdout=out_check, check=False)
    with open('correct.cpp', 'w', encoding='utf-8') as out_corr:
        subprocess.run(['echo', cpp_files[2]], stdout=out_corr, check=False)
    with open('wrong.cpp', 'w', encoding='utf-8') as out_wrong:
        subprocess.run(['echo', cpp_files[3]], stdout=out_wrong, check=False)

    
    # executing stress-test 
    dbg_res = stresstest(safety, testcase, timelimit)
    
    # updating test row adding tester's result
    cur.execute("UPDATE submission SET result = %s WHERE test_id = %s ;",
                (str(dbg_res), str(test_id)))

    # commiting the transaction
    conn.commit()

    # deleting temporary files and directory
    os.chdir('../')
    subprocess.call(['rm', '-r', f'id_{test_id}/'])
    
    return (test_id, dbg_res)
    
    
# Returns the details of a specific submission
# id: the id of the submission returned
def getSub(subid):
    # using heroku API-KEY to obtain current database_url
    app = heroku3.from_key(API_KEY).app('multiprocessing-stress-tester')
    DATABASE_URL = app.config()['DATABASE_URL']

    # connecting to the database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # executing select to have rows for the table
    cur.execute("SELECT * FROM submission WHERE test_id = %s ;", (str(subid), ))
    row = cur.fetchone()
    return row


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
