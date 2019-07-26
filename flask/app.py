from flask import Flask, jsonify
from proj.tasks import getnumber
from proj.celery import app as celery

app = Flask(__name__)

@app.route('/number')
def number():
    task = getnumber.delay()
    return task.id

@app.route('/result/<task_id>')
def result(task_id):
    task = getnumber.AsyncResult(task_id)
    result = task.get(timeout = 3)
    response = {
        'state': task.state,
        'number': result,
    }
    return jsonify(response)
