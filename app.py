from flask import Flask, request, render_template, jsonify
from datetime import datetime
import csv

app = Flask(__name__)

@app.route("/")
def todo():
    return render_template("index.html")

@app.route("/api/log_new_task", methods=['POST'])
def lognewtask():
    new_task = request.args.get('new_task', type=str)
    with open(file='./logs/tasks_added.csv', mode='a', newline='') as log_CSV:
        log_CSV_writer = csv.writer(log_CSV, delimiter=',', quotechar='"')
        log_CSV_writer.writerow([str(datetime.now()), new_task])
    return jsonify("{\"result\": task_added}")

app.run(debug=True)