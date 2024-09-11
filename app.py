import os
import shutil
import sqlite3
from flask import Flask, render_template, request, redirect
from celery import Celery
from werkzeug.utils import secure_filename
from plugin import run
from setup_db import setup

DB_PATH = 'db/db.sqlite'

setup()

app = Flask(__name__)
celery = Celery('tasks', broker='redis://redis:6379')


UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    print(request.files)
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    roll_no = request.form.get('rollno')
    assignment = request.form.get('assignment')
    # secure filename to prevent security issues
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    task = run_tests.delay(roll_no, assignment, filename, 'tests/test1.py')
    print(task)
    return redirect('/')

@app.route('/results')
def results():

    conn = sqlite3.connect(DB_PATH)
    curse = conn.cursor()

    res = curse.execute("SELECT * FROM result WHERE roll_no = ?", (251684000,))


    return render_template('results.html', test_cases=res)

@celery.task(name="run_tests")
def run_tests(roll_no, assignment, filename, test_file):
    shutil.copyfile(test_file, 'tmp/test.py')
    shutil.copyfile(f'uploads/{filename}', 'tmp/to_test.py')

    results = run('tmp/test.py')
    print(results.reports)
    
    for i in os.listdir('tmp'):
        if i == '.keep':
            continue
        try:
            os.remove(f"tmp/{i}")
        except:
            continue

    conn = sqlite3.connect(DB_PATH)
    curse = conn.cursor()

    curse.execute("""
        INSERT INTO result(roll_no, assignment, passed, failed) VALUES (?, ?, ?, ?)
    """, (roll_no, assignment, results.passed, results.failed))
    conn.commit()

    return results.passed, results.failed

if __name__ == "__main__":
    app.run()
