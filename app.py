import os
from flask import Flask, redirect, request, render_template, jsonify, session
from datetime import datetime
import csv

app = Flask(__name__)
app.secret_key = '123'

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/api/login", methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']

    userIsAuthenticated = False
    with open("users.csv", "r") as usersFileReader:
        usersFileCsvReader = csv.reader(usersFileReader)
        for user in usersFileCsvReader:
            if username == user[0] and password == user[1]:
                userIsAuthenticated = True
                break
    
    if userIsAuthenticated:
        session['username'] = username
        return jsonify( { "userIsAuthenticated": userIsAuthenticated } )
    else:
        return jsonify( { "userIsAuthenticated": userIsAuthenticated } ), 401

@app.route("/api/logout", methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify( { "sessionClosed": True })

@app.route("/adduser", methods=['GET'])
def addUserPage():
    return render_template("adduser.html")

@app.route("/api/adduser", methods=['POST'])
def adduser():
    username = request.form['username']
    password = request.form['password']

    os.makedirs(f"./states/{username}/")
    for file in ['incomplete_tasks', 'completed_tasks']:
        with open(f"./states/{username}/{file}.csv", 'x'):
            pass

    os.makedirs(f"./logs/{username}/")
    for file in ['tasks_incomplete', 'tasks_completed', 'tasks_deleted', 'tasks_edited', 'tasks_cleared']:
        with open(f"./logs/{username}/{file}.csv", 'x'):
            pass

    with open("users.csv", "a", newline='') as usersFile:
        usersFileCsvWriter = csv.writer(usersFile)
        usersFileCsvWriter.writerow([username, password])

    return redirect('/')

@app.route("/api/populateuserdata", methods=['GET'])
def getUserData():
    incomplete_tasks, completed_tasks = populateUserData(session.get('username'))
    return jsonify({ "incomplete_tasks": incomplete_tasks, "completed_tasks": completed_tasks })

@app.route("/index")
def index():
    if 'username' in session and session['username']:
        return render_template("index.html")
    else:
        return redirect('/')
    
def writeToLogsAndStates(username, file_name, task, incomplete_tasks, completed_tasks):
    with open(file_name, mode='a', newline='') as log_CSV:
        log_CSV_writer = csv.writer(log_CSV, delimiter=',', quotechar='"')
        log_CSV_writer.writerow([str(datetime.now()), task])

    with open(f"./states/{username}/completed_tasks.csv", mode='w', newline='') as comp_tasks_CSV:
        comp_tasks_CSV_writer = csv.writer(comp_tasks_CSV, delimiter=',', quotechar='"')
        for key, value in completed_tasks.items():
            comp_tasks_CSV_writer.writerow([value, key])
    
    with open(f"./states/{username}/incomplete_tasks.csv", mode='w', newline='') as incomp_tasks_CSV:
        incomp_tasks_CSV_writer = csv.writer(incomp_tasks_CSV, delimiter=',', quotechar='"')
        for key, value in incomplete_tasks.items():
            incomp_tasks_CSV_writer.writerow([value, key])
    
def populateUserData(username):
    completed_tasks = {}
    with open(f"./states/{username}/completed_tasks.csv", 'r') as completedTasksFile:
        completedTasksFileCsvReader = csv.reader(completedTasksFile)
        for row in completedTasksFileCsvReader:
            completed_tasks.update({row[1]: row[0]})

    incomplete_tasks = {}
    with open(f"./states/{username}/incomplete_tasks.csv", 'r') as incompleteTasksFile:
        incompleteTasksFileCsvReader = csv.reader(incompleteTasksFile)
        for row in incompleteTasksFileCsvReader:
            incomplete_tasks.update({row[1]: row[0]})

    return incomplete_tasks, completed_tasks
    
@app.route("/api/log_task", methods=['POST'])
def logTask():
    task = request.json.get('task')
    task_type = request.json.get('type')
    username = session.get('username')
    incomplete_tasks, completed_tasks = populateUserData(username)

    if task_type == 'incomplete':
        file_name = f'./logs/{username}/tasks_incomplete.csv'
        incomplete_tasks.update({task: str(datetime.now())})
        if task in completed_tasks:
            completed_tasks.pop(task)
    elif task_type == 'delete':
        file_name = f'./logs/{username}/tasks_deleted.csv'
        if task in incomplete_tasks:
            incomplete_tasks.pop(task)
        if task in completed_tasks:
            completed_tasks.pop(task)
    elif task_type == 'edit':
        file_name = f'./logs/{username}/tasks_edited.csv'

        original_task = task.split(" -> ")[0]
        edited_task = task.split(" -> ")[1]

        if original_task in incomplete_tasks:
            incomplete_tasks.pop(original_task)
            incomplete_tasks.update({edited_task: str(datetime.now())})
        else:
            completed_tasks.pop(original_task)
            completed_tasks.update({edited_task: str(datetime.now())})
    elif task_type == 'complete':
        file_name = f'./logs/{username}/tasks_completed.csv'
        incomplete_tasks.pop(task)
        completed_tasks.update({task: str(datetime.now())})
    else:
        file_name = f'./logs/{username}/tasks_cleared.csv'
        incomplete_tasks = {}
        completed_tasks = {}
    
    writeToLogsAndStates(username, file_name, task, incomplete_tasks, completed_tasks)
        
    return jsonify("{\"result\": task successfully logged}")

if __name__ == "__main__":
    app.run(debug=True)