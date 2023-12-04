from flask import Flask, request, render_template, jsonify
from datetime import datetime
import csv

incomplete_tasks = {}
completed_tasks = {}

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/api/login", methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']

    userIsValid = False
    with open("users.csv", "r") as usersFileReader:
        usersFileCsvReader = csv.reader(usersFileReader)
        for user in usersFileCsvReader:
            if username == user[0] and password == user[1]:
                userIsValid = True
                break
            
    if userIsValid:
        return jsonify( { "userIsValid": userIsValid } )
    else:
        return jsonify( { "userIsValid": userIsValid } ), 401

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/api/log_task", methods=['POST'])
def logTask():
    task = request.json.get('task')
    task_type = request.json.get('type')

    global incomplete_tasks
    global completed_tasks

    if task_type == 'incomplete':
        file_name = './logs/tasks_incomplete.csv'
        incomplete_tasks.update({task: str(datetime.now())})
        if task in completed_tasks:
            completed_tasks.pop(task)
    elif task_type == 'delete':
        file_name = './logs/tasks_deleted.csv'
        if task in incomplete_tasks:
            incomplete_tasks.pop(task)
        if task in completed_tasks:
            completed_tasks.pop(task)
    elif task_type == 'edit':
        file_name = './logs/tasks_edited.csv'

        original_task = task.split(" -> ")[0]
        edited_task = task.split(" -> ")[1]

        if original_task in incomplete_tasks:
            incomplete_tasks.pop(original_task)
            incomplete_tasks.update({edited_task: str(datetime.now())})
        else:
            completed_tasks.pop(original_task)
            completed_tasks.update({edited_task: str(datetime.now())})
    elif task_type == 'complete':
        file_name = './logs/tasks_completed.csv'
        incomplete_tasks.pop(task)
        completed_tasks.update({task: str(datetime.now())})
    else:
        file_name = './logs/tasks_cleared.csv'
        incomplete_tasks = {}
        completed_tasks = {}

    with open(file_name, mode='a', newline='') as log_CSV:
        log_CSV_writer = csv.writer(log_CSV, delimiter=',', quotechar='"')
        log_CSV_writer.writerow([str(datetime.now()), task])

    with open("./state/completed_tasks.csv", mode='w', newline='') as comp_tasks_CSV:
        comp_tasks_CSV_writer = csv.writer(comp_tasks_CSV, delimiter=',', quotechar='"')
        for key, value in completed_tasks.items():
            comp_tasks_CSV_writer.writerow([value, key])
    
    with open("./state/incomplete_tasks.csv", mode='w', newline='') as incomp_tasks_CSV:
        incomp_tasks_CSV_writer = csv.writer(incomp_tasks_CSV, delimiter=',', quotechar='"')
        for key, value in incomplete_tasks.items():
            incomp_tasks_CSV_writer.writerow([value, key])
        
    return jsonify("{\"result\": task successfully logged}")

if __name__ == "__main__":
    app.run(debug=True)